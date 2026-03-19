import requests

API_KEY = "pub_38deae75340b497db8a36d8210c9e354"

def fetch_news():
    url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&language=en"

    response = requests.get(url)
    data = response.json()

    articles = data.get("results", [])

    print(f"Fetched {len(articles)} articles")

    cleaned_articles = []

    for article in articles:
        cleaned = {
            "title": article.get("title"),
            "description": article.get("description"),
            "source": article.get("source_name"),
            "date": article.get("pubDate")
        }
        cleaned_articles.append(cleaned)

    return cleaned_articles


from sentiment import get_sentiment

if __name__ == "__main__":
    news = fetch_news()

    for article in news[:5]:
        sentiment = get_sentiment(article["description"])

        print("\nTitle:", article["title"])
        print("Sentiment:", sentiment)