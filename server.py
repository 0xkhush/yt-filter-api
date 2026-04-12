"""
server.py — Flask API server for YouTube content classification.

Endpoints:
  POST /predict — Classify a video as constructive or non-constructive
  GET  /health  — Health check

Loads TF-IDF vectorizer and Logistic Regression model at startup.
"""

import os
import re
import string
import joblib
import numpy as np
from scipy.sparse import hstack, csr_matrix
from flask import Flask, request, jsonify
from flask_cors import CORS


# ─── App Setup ────────────────────────────────────────────────────────────────

app = Flask(__name__)
CORS(app)  # Allow requests from browser extensions

# ─── Load Model ──────────────────────────────────────────────────────────────

MODEL_DIR = "model"
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")
CLASSIFIER_PATH = os.path.join(MODEL_DIR, "classifier.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")


def load_model():
    """Load the trained model, vectorizer, and scaler."""
    for path in [VECTORIZER_PATH, CLASSIFIER_PATH, SCALER_PATH]:
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"{path} not found. Run `python train_model.py` first."
            )
    vectorizer = joblib.load(VECTORIZER_PATH)
    classifier = joblib.load(CLASSIFIER_PATH)
    scaler = joblib.load(SCALER_PATH)
    return vectorizer, classifier, scaler


print("🔄 Loading model...")
vectorizer, classifier, scaler = load_model()
print("✅ Model loaded successfully!")


# ─── Text Preprocessing ──────────────────────────────────────────────────────

def preprocess_text(text: str) -> str:
    """Clean and normalize text — must match training preprocessing."""
    text = str(text).lower()
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_engineered_features(raw_text: str) -> np.ndarray:
    """Extract hand-crafted features from raw text — must match training."""
    text = str(raw_text)
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

    return np.array([[
        caps_ratio, exclamation_count, question_count,
        text_length, emoji_count, word_count,
        avg_word_len, all_caps_words,
    ]])


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "model_loaded": True}), 200


@app.route("/predict", methods=["POST"])
def predict():
    """
    Classify a YouTube video as constructive or non-constructive.

    Request JSON:
    {
        "channel": "3Blue1Brown",
        "title": "Linear Algebra Explained Visually",
        "description": "A visual guide to understanding linear transformations..."
    }

    Response JSON:
    {
        "constructive": true,
        "confidence": 0.94,
        "message": "yes"
    }
    """
    # ── Validate Input ────────────────────────────────────────────────────────
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    channel = data.get("channel", "")
    title = data.get("title", "")
    description = data.get("description", "")

    if not title and not description:
        return jsonify({"error": "At least 'title' or 'description' is required"}), 400

    # ── Preprocess ──────────────────────────────────────────────────────────
    combined_raw = f"{channel} {title} {description}"
    cleaned_text = preprocess_text(combined_raw)

    # ── Predict ─────────────────────────────────────────────────────────────
    text_vector = vectorizer.transform([cleaned_text])
    eng_features = extract_engineered_features(combined_raw)
    eng_scaled = scaler.transform(eng_features)
    combined = hstack([text_vector, csr_matrix(eng_scaled)])

    prediction = classifier.predict(combined)[0]
    probabilities = classifier.predict_proba(combined)[0]

    is_constructive = bool(prediction == 1)
    confidence = float(max(probabilities))

    return jsonify({
        "constructive": is_constructive,
        "confidence": round(confidence, 4),
        "message": "yes" if is_constructive else "no",
    }), 200


# ─── Error Handlers ──────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Server starting on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
