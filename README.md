# Twitter Sentiment Analysis

A sentiment analysis project that fetches live tweets using the Twitter API and analyzes their sentiment using **TextBlob** and **VADER (NLTK)**.  
The results are visualized with **matplotlib** and a **Streamlit web app**.

---

## ✨ Features
- 🔑 Fetch tweets using **Twitter API v2** via Tweepy  
- 🧹 Preprocess tweets (remove links, mentions, hashtags, punctuation, etc.)  
- 😊 Sentiment analysis using:
  - TextBlob (polarity, subjectivity)
  - VADER (positive, neutral, negative)
- 📊 Visualizations:
  - Sentiment distribution (pie chart)
  - Word cloud of most common words
- 🌐 Streamlit front end (no need to run in terminal)

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Manpreet29/Twitter-Sentiment-Analysis
cd Twitter-Sentiment-Analysis
```

### 2. Create & activate virtual environment (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a file named .env in the project root with your Twitter API Bearer Token:

```bash
BEARER_TOKEN=your_twitter_bearer_token_here
```

### 5. Run the Streamlit app
```bash
streamlit run app.py
```

This launches the web app at http://localhost:8501/.

---

### 📂 Project Structure
```bash
Twitter-Sentiment-Analysis/
│── app.py              # Streamlit web app
│── fetcher.py          # Fetch tweets from Twitter API
│── preprocessing.py    # Clean & preprocess tweets
│── sentiment.py        # Apply TextBlob & VADER sentiment analysis
│── visualize.py        # Plot pie chart & word cloud
│── main.py             # Command-line pipeline runner
│── requirements.txt    # Python dependencies
│── .gitignore          # Ignored files (includes .env, venv, data/)
│── README.md           # Project documentation
│── LICENSE             # MIT License
└── data/               # (ignored) folder for tweets CSV
```

---

### 🖥️ Example Visualizations

Pie chart: Sentiment distribution

Word cloud: Frequently used words

<img width="1919" height="965" alt="image" src="https://github.com/user-attachments/assets/719ab8c7-5d96-468e-b267-df6cc33c6082" />
<img width="869" height="598" alt="image" src="https://github.com/user-attachments/assets/4726659d-b4a8-4d4d-831b-b87eabe42837" />
<img width="1871" height="896" alt="image" src="https://github.com/user-attachments/assets/0d83553b-3ca8-40f7-98ff-df9af0a069d1" />
<img width="858" height="463" alt="image" src="https://github.com/user-attachments/assets/b3140286-1a0b-4530-8ac5-1f32f80d227d" />


---

### 📜 License
This project is licensed under the MIT License — see the LICENSE file for details.

---

### 🙌 Acknowledgements

Tweepy for Twitter API access

TextBlob for NLP sentiment analysis

VADER Sentiment (part of NLTK)

Streamlit for the web UI
