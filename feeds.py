import feedparser

# Reuters ne publie plus de flux RSS public depuis 2020.
# Cette adresse Google News ne renvoie que des articles du site reuters.com.
FEEDS = (
    {
        "source": "BBC News",
        "url": "https://feeds.bbci.co.uk/news/rss.xml",
    },
    {
        "source": "Reuters",
        "url": (
            "https://news.google.com/rss/search"
            "?q=when:24h+site:reuters.com&ceid=US:en&hl=en-US&gl=US"
        ),
    },
)


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


def print_articles(articles: list[dict[str, str]]) -> None:
    print(f"{len(articles)} articles")
    for article in articles:
        print(f"[{article['source']}] {article['title']}")
        print(f"  {article['date']}")
        print(f"  {article['link']}")
        print()


if __name__ == "__main__":
    print_articles(fetch_articles())
