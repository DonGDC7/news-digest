import trafilatura

PREVIEW_PARAGRAPHS = 3


def fetch_article_text(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""
    text = trafilatura.extract(
        downloaded,
        url=url,
        include_comments=False,
        include_tables=False,
    )
    if not text or "enable js" in text.lower():
        return ""
    paragraphs = [part.strip() for part in text.splitlines() if len(part.strip()) >= 40]
    return "\n\n".join(paragraphs)


def preview_text(text: str) -> str:
    paragraphs = [part for part in text.split("\n\n") if part]
    return "\n\n".join(paragraphs[:PREVIEW_PARAGRAPHS])


def print_article_preview(article: dict[str, str]) -> None:
    print(f"Texte de l'article : {article['title']}")
    text = fetch_article_text(article["link"])
    if not text:
        print("texte introuvable")
        return
    print(preview_text(text))
    print()
    total = len([part for part in text.split("\n\n") if part])
    print(f"{total} paragraphes au total, aperçu des {PREVIEW_PARAGRAPHS} premiers")


if __name__ == "__main__":
    from feeds import fetch_articles, keep_recent

    recent = keep_recent(fetch_articles())
    if not recent:
        print("aucun article à lire")
    else:
        print_article_preview(recent[0])
