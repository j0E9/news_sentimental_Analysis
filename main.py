import streamlit as st
import psycopg2
import pandas as pd
import os

def get_data():
    conn = psycopg2.connect(
        dbname="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port="5432"
    )

    query = "SELECT * FROM news ORDER BY created_at DESC;"
    df = pd.read_sql(query, conn)

    conn.close()
    return df


# DB connection
# def get_data():
#     conn = psycopg2.connect(
#         dbname="news_db",
#         user="postgres",
#         password="Joe72022@",
#         host="host.docker.internal",
#         port="5432"
#     )



    query = "SELECT * FROM news ORDER BY created_at DESC;"
    df = pd.read_sql(query, conn)

    conn.close()
    return df


# Load data
df = get_data()

# ---------------- UI ----------------
st.title("📰 News Sentiment Dashboard")

# 🔹 Add sentiment label
def get_label(val):
    if val > 0:
        return "Positive"
    elif val < 0:
        return "Negative"
    else:
        return "Neutral"

df["sentiment_label"] = df["sentiment"].apply(get_label)

# 🔹 Color function
def color_label(val):
    if val == "Positive":
        return 'color: green; font-weight: bold'
    elif val == "Negative":
        return 'color: red; font-weight: bold'
    else:
        return 'color: gray; font-weight: bold'

# 🔹 Style dataframe
styled_df = df.style.applymap(color_label, subset=["sentiment_label"])

# ---------------- Dashboard ----------------

st.subheader("📊 Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total", len(df))
col2.metric("Positive", (df["sentiment"] > 0).sum())
col3.metric("Negative", (df["sentiment"] < 0).sum())

# ---------------- Chart ----------------
st.subheader("📈 Sentiment Chart")
st.bar_chart(df["sentiment"])

# ---------------- Table ----------------
st.subheader("🗂️ News Data")

# Step 1: Select columns FIRST
display_df = df[["title", "sentiment", "sentiment_label", "source"]]

# Step 2: Apply styling (use .map instead of applymap)
styled_df = display_df.style.map(color_label, subset=["sentiment_label"])

# Step 3: Display
st.dataframe(styled_df, use_container_width=True)