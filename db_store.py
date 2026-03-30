import psycopg2

def insert_news(article, sentiment):
    try:
        conn = psycopg2.connect(
            dbname="news_db",
            user="postgres",
            password="Joe72022@",
            host="localhost",
            port="5432"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO news (title, description, sentiment, source, published_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                article["title"],
                article["description"],
                sentiment,
                article["source"],
                article["date"]
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print("DB Error:", e)