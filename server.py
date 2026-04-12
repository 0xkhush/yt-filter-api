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
from flask import Flask, request, jsonify
from flask_cors import CORS


# ─── App Setup ────────────────────────────────────────────────────────────────

app = Flask(__name__)
CORS(app)  # Allow requests from browser extensions

# ─── Load Model ──────────────────────────────────────────────────────────────

MODEL_DIR = "model"
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")
CLASSIFIER_PATH = os.path.join(MODEL_DIR, "classifier.pkl")


def load_model():
    """Load the trained model and vectorizer."""
    if not os.path.exists(VECTORIZER_PATH) or not os.path.exists(CLASSIFIER_PATH):
        raise FileNotFoundError(
            "Model files not found. Run `python train_model.py` first."
        )
    vectorizer = joblib.load(VECTORIZER_PATH)
    classifier = joblib.load(CLASSIFIER_PATH)
    return vectorizer, classifier


print("🔄 Loading model...")
vectorizer, classifier = load_model()
print("✅ Model loaded successfully!")


# ─── Text Preprocessing ──────────────────────────────────────────────────────

def preprocess_text(text: str) -> str:
    """Clean and normalize text — must match training preprocessing."""
    text = str(text).lower()
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


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

    # ── Preprocess ────────────────────────────────────────────────────────────
    combined_text = f"{channel} {title} {description}"
    cleaned_text = preprocess_text(combined_text)

    # ── Predict ───────────────────────────────────────────────────────────────
    text_vector = vectorizer.transform([cleaned_text])
    prediction = classifier.predict(text_vector)[0]
    probabilities = classifier.predict_proba(text_vector)[0]

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
