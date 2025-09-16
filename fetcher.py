import os
import tweepy
import pandas as pd
from dotenv import load_dotenv

# Load API keys
load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")

# Authenticate
client = tweepy.Client(bearer_token=bearer_token)
print("Connected to Twitter API ✅")

# Search for tweets
def fetch_tweets(keyword: str, num_tweets: int, output_file: str = "data/tweets.csv", api = None):
    if api is None:
        raise ValueError("Twitter API object not provided. Pass 'api' from st.secrets in Streamlit.")
    
    query = f"{keyword} -is:retweet lang:en"
    tweets = client.search_recent_tweets(query=query, max_results=num_tweets)

    tweet_data = []

    if tweets.data:  # Only if tweets exist
        for tweet in tweets.data:
            tweet_data.append([tweet.id, tweet.text])

        # Save to CSV
        df = pd.DataFrame(tweet_data, columns=["id", "text"])
        df.to_csv("data/tweets.csv", index=False, encoding="utf-8")
        print(f"✅ Saved {len(df)} tweets to data/tweets.csv")
    else:
        print("⚠️ No tweets found for this query.")
