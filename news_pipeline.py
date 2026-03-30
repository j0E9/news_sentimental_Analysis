from news_fetch import fetch_news
from sentiment import get_sentiment
from db_store import insert_news

def run_pipeline():
    articles = fetch_news()

    for article in articles:
        sentiment = get_sentiment(article["description"])

        insert_news(article, sentiment)

    print("Pipeline completed")


if __name__ == "__main__":
    run_pipeline()