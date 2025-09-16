# app.py
import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import tweepy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# pipeline functions from your project
from fetcher import fetch_tweets      # must accept (keyword, num_tweets, output_file)
from preprocessing import preprocess_csv
from sentiment import sentiment_csv

# ensure required nltk data is available
nltk.download('vader_lexicon', quiet=True)

# Page config
st.set_page_config(page_title="Twitter Sentiment Analysis", layout="wide")
st.title("🐦 Twitter Sentiment Analysis")

# File paths
RAW_PATH = "data/tweets.csv"
CLEAN_PATH = "data/tweets_clean.csv"
SENT_PATH = "data/tweets_sentiment.csv"

# Sidebar: inputs
with st.sidebar:
    st.header("Fetch options")
    keyword = st.text_input("Keyword", value="Apple")
    num_tweets = st.number_input("Number of tweets (total)", min_value=10, max_value=1000, value=20, step=10)
    use_saved = st.checkbox("Use saved tweets file if present (skip fetching)", value=True)
    refetch = st.checkbox("Force refetch (overwrite saved file)", value=False)
    run_btn = st.button("Run analysis")

# helper plotting utilities
def plot_sentiment_pie(labels_series, title="Sentiment distribution"):
    fig, ax = plt.subplots(figsize=(2,2))
    counts = labels_series.value_counts()
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    ax.set_title(title)
    return fig

def plot_wordcloud_from_texts(texts):
    text = " ".join([str(t) for t in texts if str(t).strip()])
    if not text:
        return None
    wc = WordCloud(width=400, height=200, background_color="white").generate(text)
    fig, ax = plt.subplots(figsize=(5,2))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    return fig

def infer_label_series(df):
    # Common column checks
    if "sentiment" in df.columns:
        return df["sentiment"]
    for col in ["vader_sentiment", "textblob_sentiment", "label"]:
        if col in df.columns:
            return df[col]
    # scores based columns
    if "compound" in df.columns:
        return df["compound"].apply(lambda c: "Positive" if c >= 0.05 else ("Negative" if c <= -0.05 else "Neutral"))
    if "polarity" in df.columns:
        return df["polarity"].apply(lambda p: "Positive" if p > 0 else ("Negative" if p < 0 else "Neutral"))
    # fallback: compute using Vader on clean_text
    sia = SentimentIntensityAnalyzer()
    if "clean_text" in df.columns:
        return df["clean_text"].astype(str).apply(
            lambda t: "Positive" if sia.polarity_scores(t)["compound"] >= 0.05
            else ("Negative" if sia.polarity_scores(t)["compound"] <= -0.05 else "Neutral")
        )
    # last fallback: use raw 'text' column
    if "text" in df.columns:
        return df["text"].astype(str).apply(
            lambda t: "Positive" if sia.polarity_scores(t)["compound"] >= 0.05
            else ("Negative" if sia.polarity_scores(t)["compound"] <= -0.05 else "Neutral")
        )
    # if nothing exists, return empty Series
    return pd.Series([], dtype="object")

# Run pipeline when button pressed
if run_btn:
    # Decide whether to fetch
    should_fetch = refetch or (not use_saved) or (not os.path.exists(RAW_PATH))
    if should_fetch:
        try:
            with st.spinner(f"Fetching {num_tweets} tweets for '{keyword}'..."):
                fetch_tweets(keyword, num_tweets, RAW_PATH)
        except tweepy.errors.TooManyRequests:
            st.error("Twitter API rate limit reached. Using existing tweets file if available.")
            if not os.path.exists(RAW_PATH):
                st.stop()
        except Exception as e:
            st.error(f"Error while fetching tweets: {e}")
            if not os.path.exists(RAW_PATH):
                st.stop()
    else:
        st.info(f"Using existing file: {RAW_PATH}")

    # Preprocess
    if os.path.exists(RAW_PATH):
        with st.spinner("Preprocessing tweets..."):
            preprocess_csv(RAW_PATH, CLEAN_PATH)
    else:
        st.error(f"No raw tweets file found at {RAW_PATH}")
        st.stop()

    # Sentiment analysis
    if os.path.exists(CLEAN_PATH):
        with st.spinner("Running sentiment analysis..."):
            sentiment_csv(CLEAN_PATH, SENT_PATH)
    else:
        st.error(f"No cleaned file found at {CLEAN_PATH}")
        st.stop()

    # Load results and visualize
    if os.path.exists(SENT_PATH):
        df = pd.read_csv(SENT_PATH)
        st.success("✅ Analysis complete")
        # basic info
        st.markdown(f"**Total rows in sentiment file:** {len(df)}")
        st.subheader("Sample (first 10 rows)")
        st.dataframe(df.head(10))

        # infer a label column
        labels = infer_label_series(df)
        if labels.empty:
            st.warning("Could not find or infer sentiment labels. Showing raw data only.")
        else:
            fig_pie = plot_sentiment_pie(labels, title="Sentiment distribution")
            st.pyplot(fig_pie)

            # bar chart
            counts = labels.value_counts()
            st.bar_chart(counts)

        # wordcloud (uses cleaned text if available)
        text_column = None
        if "clean_text" in df.columns:
            text_column = df["clean_text"].astype(str).tolist()
        elif "text" in df.columns:
            text_column = df["text"].astype(str).tolist()

        if text_column:
            fig_wc = plot_wordcloud_from_texts(text_column)
            if fig_wc:
                st.subheader("Word Cloud")
                st.pyplot(fig_wc)

        # download button
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download sentiment CSV", csv_bytes, file_name="tweets_sentiment.csv", mime="text/csv")

    else:
        st.error(f"No sentiment file found at {SENT_PATH}.")
