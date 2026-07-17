"""Helpers for loading a trained resume classifier and predicting categories."""

from __future__ import annotations

from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "model.pkl"
VECTORIZER_FILE = BASE_DIR / "vectorizer.pkl"


def load_classifier():
    """Load the saved model and vectorizer because the live API should not train on every request."""

    if not MODEL_FILE.exists() or not VECTORIZER_FILE.exists():
        return None, None

    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)
    return model, vectorizer


def predict_category(cleaned_text, model, vectorizer):
    """Predict the resume category because the API only needs the final label, not the raw probabilities."""

    if model is None or vectorizer is None:
        raise ValueError("Model and vectorizer must be loaded before prediction.")

    features = vectorizer.transform([cleaned_text])
    prediction = model.predict(features)
    return str(prediction[0])
