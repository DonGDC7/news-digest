from config import REQUIRED_SETTINGS, load_config
from feeds import fetch_articles, print_articles


def main() -> None:
    print("news-digest démarre")
    config = load_config()
    print("configuration chargée")
    for name in REQUIRED_SETTINGS:
        status = "présente" if config[name] else "vide"
        print(f"- {name} : {status}")
    print()
    print_articles(fetch_articles())


if __name__ == "__main__":
    main()
