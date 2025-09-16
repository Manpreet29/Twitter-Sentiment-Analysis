import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def plot_sentiment_pie(input_file: str):
    df = pd.read_csv(input_file)

    # Categorize based on VADER compound score
    df["sentiment"] = df["vader_compound"].apply(
        lambda x: "positive" if x > 0.05 else ("negative" if x < -0.05 else "neutral")
    )

    counts = df["sentiment"].value_counts()

    plt.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90)
    plt.title("Sentiment Distribution")
    plt.show()

def plot_wordcloud(input_file: str):
    df = pd.read_csv(input_file)
    text = " ".join(df["clean_text"].astype(str))

    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Word Cloud of Tweets", fontsize=16)
    plt.show()
