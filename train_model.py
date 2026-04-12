"""
train_model.py — Trains TF-IDF + Logistic Regression classifier.

Reads data/training_data.csv, trains model, saves to model/ directory.
Prints accuracy, precision, recall, F1, and confusion matrix.
"""

import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
import re
import string


def preprocess_text(text: str) -> str:
    """Clean and normalize text for vectorization."""
    text = str(text).lower()
    # Remove emojis and special unicode characters
    text = text.encode("ascii", "ignore").decode("ascii")
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    # ── Load Data ─────────────────────────────────────────────────────────────
    data_path = "data/training_data.csv"
    if not os.path.exists(data_path):
        print(f"❌ Data file not found: {data_path}")
        print("   Run `python generate_data.py` first.")
        return

    print("📂 Loading training data...")
    df = pd.read_csv(data_path)
    print(f"   Loaded {len(df)} samples")
    print(f"   Label distribution:\n{df['label'].value_counts().to_string()}\n")

    # ── Combine Features ──────────────────────────────────────────────────────
    print("🔧 Preprocessing text...")
    df["text"] = (
        df["channel_name"].fillna("")
        + " "
        + df["title"].fillna("")
        + " "
        + df["description"].fillna("")
    )
    df["text"] = df["text"].apply(preprocess_text)

    X = df["text"]
    y = df["label"]

    # ── Train/Test Split ──────────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Train: {len(X_train)} | Test: {len(X_test)}\n")

    # ── TF-IDF Vectorization ─────────────────────────────────────────────────
    print("📊 Fitting TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=10000,
        stop_words="english",
        ngram_range=(1, 2),  # unigrams + bigrams for better context
        min_df=2,
        max_df=0.95,
        sublinear_tf=True,
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    print(f"   Vocabulary size: {len(vectorizer.vocabulary_)}")
    print(f"   Feature matrix: {X_train_tfidf.shape}\n")

    # ── Train Classifier ─────────────────────────────────────────────────────
    print("🧠 Training Logistic Regression...")
    classifier = LogisticRegression(
        solver="liblinear",
        max_iter=1000,
        C=1.0,
        random_state=42,
    )
    classifier.fit(X_train_tfidf, y_train)
    print("   Training complete!\n")

    # ── Evaluate ──────────────────────────────────────────────────────────────
    y_pred = classifier.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("=" * 50)
    print("📈 MODEL EVALUATION RESULTS")
    print("=" * 50)
    print(f"  Accuracy:  {accuracy:.4f} ({accuracy * 100:.1f}%)")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    print()

    print("📋 Classification Report:")
    print(
        classification_report(
            y_test, y_pred, target_names=["Non-constructive", "Constructive"]
        )
    )

    print("🔢 Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  TN={cm[0][0]}  FP={cm[0][1]}")
    print(f"  FN={cm[1][0]}  TP={cm[1][1]}")
    print()

    # ── Save Model ────────────────────────────────────────────────────────────
    os.makedirs("model", exist_ok=True)

    vectorizer_path = "model/vectorizer.pkl"
    classifier_path = "model/classifier.pkl"

    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(classifier, classifier_path)

    # Print file sizes
    vec_size = os.path.getsize(vectorizer_path) / (1024 * 1024)
    clf_size = os.path.getsize(classifier_path) / (1024 * 1024)

    print(f"💾 Model saved:")
    print(f"   {vectorizer_path} ({vec_size:.2f} MB)")
    print(f"   {classifier_path} ({clf_size:.2f} MB)")
    print(f"   Total: {vec_size + clf_size:.2f} MB")
    print("\n✅ Training complete! Run `python server.py` to start the API.")


if __name__ == "__main__":
    main()
