<<<<<<< HEAD
import re


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
=======
"""Text cleaning helpers for resume screening and skill extraction."""

from __future__ import annotations

import math
import re

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize

    # These downloads only need to run once on a machine; after that NLTK keeps the data locally.
    nltk.download("stopwords", quiet=True)
    nltk.download("wordnet", quiet=True)
    nltk.download("punkt", quiet=True)

    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        nltk.download("punkt_tab", quiet=True)

    STOPWORDS = set(stopwords.words("english"))
    LEMMATIZER = WordNetLemmatizer()
    NLTK_AVAILABLE = True
except Exception:
    # If the local NLTK installation is broken, keep the module usable with a simple fallback path.
    STOPWORDS = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "that",
        "the",
        "this",
        "to",
        "was",
        "were",
        "with",
    }
    LEMMATIZER = None
    NLTK_AVAILABLE = False


def _lemmatize_token(token):
    """Lemmatize a token with NLTK when available, otherwise return the token unchanged."""

    if NLTK_AVAILABLE:
        return LEMMATIZER.lemmatize(token)
    return token


def _tokenize_text(text):
    """Tokenize text with NLTK when available, otherwise fall back to a simple whitespace split."""

    if NLTK_AVAILABLE:
        try:
            return word_tokenize(text)
        except LookupError:
            return text.split()
    return text.split()


def clean_text(raw_text):
    """Normalize resume text so the downstream classifier and skill matcher see consistent words."""

    if raw_text is None or (isinstance(raw_text, float) and math.isnan(raw_text)):
        return ""

    text = str(raw_text).lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", " ", text)
    text = re.sub(
        r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b",
        " ",
        text,
    )
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return ""

    tokens = _tokenize_text(text)

    cleaned_tokens = []
    for token in tokens:
        if token in STOPWORDS:
            continue
        lemmatized_token = _lemmatize_token(token)
        if lemmatized_token:
            cleaned_tokens.append(lemmatized_token)

    return " ".join(cleaned_tokens).strip()


if __name__ == "__main__":
    sample_text = "Contact me at jane.doe@example.com, visit https://example.com, or call +1 555-123-4567. Skilled in Machine Learning, Python, and teamwork."
    print("Original:")
    print(sample_text)
    print("\nCleaned:")
    print(clean_text(sample_text))
>>>>>>> origin/main
