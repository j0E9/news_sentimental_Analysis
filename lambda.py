import requests
import psycopg2
from datetime import datetime

# 🔹 CONFIG
DB_HOST = "newsdb.cvmq2ycosc1l.ap-south-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "iXVOs6zVMHxACgsMbDdL"

NEWS_API_KEY = "pub_38deae75340b497db8a36d8210c9e354"

def lambda_handler(event, context):
    try:
        # 1. Fetch news
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        articles = response.json()["articles"]

        # 2. Connect DB
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()

        # 3. Process & insert
        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")

            # Simple sentiment logic
            sentiment = 0
            if "good" in title.lower():
                sentiment = 1
            elif "bad" in title.lower():
                sentiment = -1

            cursor.execute("""
                INSERT INTO news (title, description, sentiment, source, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                title,
                description,
                sentiment,
                article.get("source", {}).get("name", ""),
                datetime.utcnow()
            ))

        conn.commit()
        cursor.close()
        conn.close()

        return {"status": "success"}

    except Exception as e:
        print(str(e))
        return {"status": "error", "message": str(e)}