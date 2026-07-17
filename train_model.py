"""Standalone training script for the resume category classifier."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from preprocessing import clean_text

try:
    import matplotlib.pyplot as plt

    try:
        import seaborn as sns
    except ImportError:
        sns = None
    HAS_PLOTTING = True
except ImportError:
    plt = None
    sns = None
    HAS_PLOTTING = False


BASE_DIR = Path(__file__).resolve().parent
DATASET_FILE = BASE_DIR / "UpdatedResumeDataSet.csv"
MODEL_FILE = BASE_DIR / "model.pkl"
VECTORIZER_FILE = BASE_DIR / "vectorizer.pkl"
CONFUSION_MATRIX_FILE = BASE_DIR / "confusion_matrix.png"


def plot_confusion_matrix(y_test, y_pred, labels):
    """Save a confusion matrix image because it gives an easy visual check of model mistakes."""

    if not HAS_PLOTTING:
        print("Matplotlib is not installed, so the confusion matrix plot was skipped.")
        return

    matrix = confusion_matrix(y_test, y_pred, labels=labels)

    plt.figure(figsize=(12, 8))
    if sns is not None:
        sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    else:
        plt.imshow(matrix, cmap="Blues")
        plt.colorbar()
        plt.xticks(range(len(labels)), labels, rotation=45, ha="right")
        plt.yticks(range(len(labels)), labels)
        for row_index in range(matrix.shape[0]):
            for col_index in range(matrix.shape[1]):
                plt.text(col_index, row_index, matrix[row_index, col_index], ha="center", va="center")

    plt.title("Resume Category Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(CONFUSION_MATRIX_FILE, dpi=200)
    plt.close()


def main():
    """Train and save the classifier because the live API should load a pre-trained model instead of fitting one."""

    if not DATASET_FILE.exists():
        print(f"Dataset not found: {DATASET_FILE}")
        print("Place UpdatedResumeDataSet.csv in the project root before running this script.")
        return

    data = pd.read_csv(DATASET_FILE)

    if "Resume" not in data.columns or "Category" not in data.columns:
        raise ValueError("The dataset must contain 'Resume' and 'Category' columns.")

    data = data.dropna(subset=["Resume", "Category"]).copy()
    data["cleaned_resume"] = data["Resume"].apply(clean_text)

    vectorizer = TfidfVectorizer(max_features=5000)
    features = vectorizer.fit_transform(data["cleaned_resume"])
    labels = data["Category"]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    model = SVC(kernel="linear")
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    print(classification_report(y_test, y_pred))

    unique_labels = sorted(labels.unique())
    plot_confusion_matrix(y_test, y_pred, unique_labels)

    joblib.dump(model, MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)

    print(f"Saved model to {MODEL_FILE}")
    print(f"Saved vectorizer to {VECTORIZER_FILE}")
    if HAS_PLOTTING:
        print(f"Saved confusion matrix to {CONFUSION_MATRIX_FILE}")


if __name__ == "__main__":
    main()
