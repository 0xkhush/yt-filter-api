"""
train_model.py — Trains TF-IDF + Logistic Regression classifier.

Reads data/training_data.csv, trains model, saves to model/ directory.
Prints accuracy, precision, recall, F1, and confusion matrix.
Uses TF-IDF (trigrams) + engineered features for better accuracy.
"""

import os
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
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


def extract_engineered_features(raw_texts):
    """
    Extract hand-crafted features from raw (un-preprocessed) text.
    These capture stylistic signals that TF-IDF misses:
    - Clickbait tends to have MORE caps, exclamations, questions, emojis
    - Educational content tends to be longer, calmer, no caps abuse
    """
    features = []
    for text in raw_texts:
        text = str(text)
        total_chars = max(len(text), 1)
        alpha_chars = sum(1 for c in text if c.isalpha())
        upper_chars = sum(1 for c in text if c.isupper())

        caps_ratio = upper_chars / max(alpha_chars, 1)
        exclamation_count = text.count("!")
        question_count = text.count("?")
        text_length = len(text)
        emoji_count = sum(1 for c in text if ord(c) > 127)
        word_count = len(text.split())
        avg_word_len = sum(len(w) for w in text.split()) / max(word_count, 1)
        all_caps_words = sum(1 for w in text.split() if w.isupper() and len(w) > 1)

        features.append([
            caps_ratio,
            exclamation_count,
            question_count,
            text_length,
            emoji_count,
            word_count,
            avg_word_len,
            all_caps_words,
        ])
    return np.array(features)


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
    df["raw_text"] = (
        df["channel_name"].fillna("")
        + " "
        + df["title"].fillna("")
        + " "
        + df["description"].fillna("")
    )
    df["text"] = df["raw_text"].apply(preprocess_text)

    X_text = df["text"]
    X_raw = df["raw_text"]
    y = df["label"]

    # ── Train/Test Split ──────────────────────────────────────────────────────
    X_text_train, X_text_test, y_train, y_test, X_raw_train, X_raw_test = train_test_split(
        X_text, y, X_raw, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Train: {len(X_text_train)} | Test: {len(X_text_test)}\n")

    # ── TF-IDF Vectorization ─────────────────────────────────────────────────
    print("📊 Fitting TF-IDF vectorizer (trigrams, 20k features)...")
    vectorizer = TfidfVectorizer(
        max_features=20000,
        stop_words="english",
        ngram_range=(1, 3),  # unigrams + bigrams + trigrams
        min_df=2,
        max_df=0.95,
        sublinear_tf=True,
    )

    X_train_tfidf = vectorizer.fit_transform(X_text_train)
    X_test_tfidf = vectorizer.transform(X_text_test)
    print(f"   Vocabulary size: {len(vectorizer.vocabulary_)}")
    print(f"   TF-IDF matrix: {X_train_tfidf.shape}")

    # ── Engineered Features ──────────────────────────────────────────────────
    print("⚙️  Extracting engineered features (caps, !, ?, length, emojis)...")
    X_train_eng = extract_engineered_features(X_raw_train.values)
    X_test_eng = extract_engineered_features(X_raw_test.values)

    scaler = StandardScaler()
    X_train_eng_scaled = scaler.fit_transform(X_train_eng)
    X_test_eng_scaled = scaler.transform(X_test_eng)

    print(f"   Engineered features: {X_train_eng.shape[1]}")

    # ── Combine All Features ─────────────────────────────────────────────────
    from scipy.sparse import csr_matrix
    X_train_combined = hstack([X_train_tfidf, csr_matrix(X_train_eng_scaled)])
    X_test_combined = hstack([X_test_tfidf, csr_matrix(X_test_eng_scaled)])
    print(f"   Combined features: {X_train_combined.shape[1]}\n")

    # ── Train Classifier ─────────────────────────────────────────────────────
    print("🧠 Training Logistic Regression (C=10)...")
    classifier = LogisticRegression(
        solver="liblinear",
        max_iter=1000,
        C=10.0,
        random_state=42,
    )
    classifier.fit(X_train_combined, y_train)
    print("   Training complete!\n")

    # ── Evaluate ──────────────────────────────────────────────────────────────
    y_pred = classifier.predict(X_test_combined)

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

    scaler_path = "model/scaler.pkl"

    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(classifier, classifier_path)
    joblib.dump(scaler, scaler_path)

    # Print file sizes
    vec_size = os.path.getsize(vectorizer_path) / (1024 * 1024)
    clf_size = os.path.getsize(classifier_path) / (1024 * 1024)
    scl_size = os.path.getsize(scaler_path) / (1024 * 1024)

    print(f"💾 Model saved:")
    print(f"   {vectorizer_path} ({vec_size:.2f} MB)")
    print(f"   {classifier_path} ({clf_size:.2f} MB)")
    print(f"   {scaler_path} ({scl_size:.2f} MB)")
    print(f"   Total: {vec_size + clf_size + scl_size:.2f} MB")
    print("\n✅ Training complete! Run `python server.py` to start the API.")


if __name__ == "__main__":
    main()
