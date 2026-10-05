from config import REQUIRED_SETTINGS, load_config
from emailer import send_digest
from feeds import fetch_articles, keep_recent, print_articles
from summarize import summarize_saved_articles


def main() -> None:
    print("news-digest démarre")
    config = load_config()
    print("configuration chargée")
    for name in REQUIRED_SETTINGS:
        status = "présente" if config[name] else "vide"
        print(f"- {name} : {status}")
    print()
    articles = fetch_articles()
    recent = keep_recent(articles)
    print(f"{len(articles)} articles lus, {len(recent)} gardés")
    print_articles(recent)
    if not recent:
        print("aucun article à lire")
        return
    summaries = summarize_saved_articles(recent)
    if not summaries:
        print("aucun résumé à envoyer")
        return
    try:
        send_digest(summaries)
    except RuntimeError as error:
        print(f"envoi impossible ({error})")


if __name__ == "__main__":
    main()
