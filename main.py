import os
import argparse
from fetcher import fetch_tweets
from preprocessing import preprocess_csv
from sentiment import sentiment_csv
from visualize import plot_sentiment_pie, plot_wordcloud

if __name__ == "__main__":
    raw_path = "data/tweets.csv"
    clean_path = "data/tweets_clean.csv"
    sentiment_path = "data/tweets_sentiment.csv"

    # Argument parser
    parser = argparse.ArgumentParser(description="Twitter Sentiment Analysis")
    parser.add_argument("--refetch", action="store_true", help="Fetch fresh tweets from Twitter API")
    args = parser.parse_args()

    # Fetch if --refetch OR file doesn't exist
    if args.refetch or not os.path.exists(raw_path):
        keyword = input("Enter keyword to search: ")
        num_tweets = int(input("Enter number of tweets to fetch: "))
        fetch_tweets(keyword, num_tweets, raw_path)
    else:
        print(f"⚠️ Using existing file: {raw_path}")

    # Step 1: Preprocess
    preprocess_csv(raw_path, clean_path)

    # Step 2: Sentiment Analysis
    sentiment_csv(clean_path, sentiment_path)

    # Step 3: Visualization
    plot_sentiment_pie(sentiment_path)
    plot_wordcloud(sentiment_path)
