import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text: str) -> dict:
    """
    Returns sentiment scores from both TextBlob and VADER.
    """
    # TextBlob
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    # VADER
    analyzer = SentimentIntensityAnalyzer()
    vader_scores = analyzer.polarity_scores(text)

    return {
        "textblob_polarity": polarity,
        "vader_neg": vader_scores["neg"],
        "vader_neu": vader_scores["neu"],
        "vader_pos": vader_scores["pos"],
        "vader_compound": vader_scores["compound"]
    }

def sentiment_csv(input_file: str, output_file: str):
    """
    Reads preprocessed tweets, applies sentiment analysis, saves new CSV.
    """
    df = pd.read_csv(input_file)

    scores = df["clean_text"].astype(str).apply(analyze_sentiment)
    scores_df = pd.DataFrame(scores.tolist())

    result = pd.concat([df, scores_df], axis=1)
    result.to_csv(output_file, index=False)
    print(f"✅ Sentiment results saved to {output_file}")
