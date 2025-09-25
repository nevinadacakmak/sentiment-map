import pandas as pd
import re
from typing import List


def ensure_nltk():
    # Import and download only when explicitly called
    import nltk
    try:
        nltk.data.find('tokenizers/punkt')
    except Exception:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except Exception:
        nltk.download('stopwords')


def clean_text(text: str) -> str:
    if not text:
        return ''
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def preprocess_data(posts: List[dict]) -> pd.DataFrame:
    """Convert list of post dicts to DataFrame and add cleaned content and simple tokens.

    Returns DataFrame with columns: id, title, content, cleaned_content, subreddit, province, created_utc, score
    """
    ensure_nltk()
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords

    rows = []
    stop_words = set(stopwords.words('english'))
    for p in posts:
        content = p.get('content') or ''
        cleaned = clean_text(content)
        tokens = [t for t in word_tokenize(cleaned) if t not in stop_words]
        rows.append({
            'id': p.get('id'),
            'title': p.get('title'),
            'content': content,
            'cleaned_content': cleaned,
            'tokens': tokens,
            'subreddit': p.get('subreddit'),
            'province': p.get('province'),
            'created_utc': p.get('created_utc'),
            'score': p.get('score')
        })

    df = pd.DataFrame(rows)
    return df


def process_data(posts: List[dict]) -> pd.DataFrame:
    # Backwards-compatible name used elsewhere
    return preprocess_data(posts)