from config import REQUIRED_SETTINGS, load_config
from emailer import send_digest, send_status
from feeds import (
    empty_day_message,
    fetch_articles,
    keep_recent,
    missing_source_notice,
    print_articles,
)
from summarize import summarize_saved_articles


def main() -> None:
    print("news-digest démarre")
    config = load_config()
    print("configuration chargée")
    for name in REQUIRED_SETTINGS:
        status = "présente" if config[name] else "vide"
        print(f"- {name} : {status}")
    print()
    articles, unavailable = fetch_articles()
    recent = keep_recent(articles)
    print(f"{len(articles)} articles lus, {len(recent)} gardés")
    print_articles(recent)
    try:
        if not recent:
            print("aucun article à lire")
            send_status(empty_day_message(unavailable))
            return
        items, problem = summarize_saved_articles(recent)
        if not items:
            print("aucun article à envoyer")
            send_status(empty_day_message(unavailable))
            return
        notice = missing_source_notice(unavailable)
        send_digest(items, "\n\n".join(part for part in (notice, problem) if part))
    except RuntimeError as error:
        print(f"envoi impossible ({error})")


if __name__ == "__main__":
    main()
