import re
import pandas as pd

def clean_tweet(text: str) -> str:
    """
    Clean tweet text by removing links, mentions, hashtags, and special characters.
    """
    text = re.sub(r"http\S+", "", text)      # remove links
    text = re.sub(r"@\w+", "", text)         # remove mentions
    text = re.sub(r"#", "", text)            # remove hashtags symbol
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)  # remove special chars
    text = text.lower().strip()              # lowercase + strip
    return text

def preprocess_csv(input_file: str, output_file: str):
    """
    Load tweets from CSV, clean them, and save to new CSV.
    """
    df = pd.read_csv(input_file)

    # assume your tweet column is named 'text' (change if different)
    df["clean_text"] = df["text"].astype(str).apply(clean_tweet)

    df.to_csv(output_file, index=False)
    print(f"✅ Preprocessed tweets saved to {output_file}")
