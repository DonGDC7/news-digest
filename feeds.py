from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

import feedparser

FEEDS = (
    {
        "source": "BBC News",
        "url": "https://feeds.bbci.co.uk/news/rss.xml",
    },
    {
        "source": "The Guardian",
        "url": "https://www.theguardian.com/world/rss",
    },
)

# Au plus 5 articles par source, publiés dans les dernières 24 heures.
MAX_AGE = timedelta(hours=24)
MAX_PER_SOURCE = 5


def fetch_articles() -> list[dict[str, str]]:
    articles = []
    for feed in FEEDS:
        parsed = feedparser.parse(feed["url"])
        if not parsed.entries:
            print(f"{feed['source']} : flux indisponible")
            continue
        for entry in parsed.entries:
            articles.append(
                {
                    "source": feed["source"],
                    "title": entry.get("title", "").strip(),
                    "link": entry.get("link", "").strip(),
                    "date": entry.get("published", "").strip(),
                }
            )
    return articles


def article_datetime(article: dict[str, str]) -> datetime | None:
    raw_date = article.get("date", "")
    if not raw_date:
        return None
    try:
        published = parsedate_to_datetime(raw_date)
    except (TypeError, ValueError, IndexError):
        return None
    if published.tzinfo is None:
        published = published.replace(tzinfo=timezone.utc)
    return published


def keep_recent(
    articles: list[dict[str, str]],
    now: datetime | None = None,
) -> list[dict[str, str]]:
    current_time = now or datetime.now(timezone.utc)
    cutoff = current_time - MAX_AGE
    fresh: list[tuple[datetime, dict[str, str]]] = []
    for article in articles:
        published = article_datetime(article)
        if published is None or published < cutoff:
            continue
        fresh.append((published, article))
    fresh.sort(key=lambda item: item[0], reverse=True)

    per_source: dict[str, list[dict[str, str]]] = {
        feed["source"]: [] for feed in FEEDS
    }
    for _, article in fresh:
        source = article["source"]
        chosen = per_source.setdefault(source, [])
        if len(chosen) >= MAX_PER_SOURCE:
            continue
        chosen.append(article)

    recent = []
    for feed in FEEDS:
        recent.extend(per_source.get(feed["source"], []))
    return recent


def print_articles(articles: list[dict[str, str]]) -> None:
    for article in articles:
        print(f"[{article['source']}] {article['title']}")
        print(f"  {article['date']}")
        print(f"  {article['link']}")
        print()


def print_recent_articles() -> None:
    articles = fetch_articles()
    recent = keep_recent(articles)
    print(f"{len(articles)} articles lus, {len(recent)} gardés")
    print_articles(recent)


if __name__ == "__main__":
    print_recent_articles()
