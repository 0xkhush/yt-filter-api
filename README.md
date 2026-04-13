# 🎯 YouTube Content Classifier API

An AI-powered Python API that classifies YouTube videos as **constructive** or **non-constructive** using Machine Learning trained on **9,000+ real YouTube videos**. Built to power a Chrome extension and deployed on a **1GB RAM Oracle VM** — fast, minimal, and production-ready.

> **Constructive** = Education, Music, News, Science & Tech → `"yes"`  
> **Non-constructive** = Gaming, Vlogs, Pranks, Clickbait, Gossip → `"no"`

---

## 🏗️ Architecture

```
┌──────────────────────┐                           ┌───────────────────────┐
│   Chrome Extension    │    POST /predict          │   Flask API Server    │
│                       │ ──────────────────────▸   │                       │
│  Content Script:      │                           │  1. TF-IDF Vectorize  │
│  • Scrapes metadata   │   { constructive: true,   │  2. Engineer Features │
│  • Pre-scans feed     │ ◂── confidence: 0.94 }    │  3. Logistic Regress. │
│                       │                           │                       │
│  Feed Pre-Scanner:    │    POST /predict/batch     │  Batch prediction     │
│  • Scans thumbnails   │ ──────────────────────▸   │  (up to 50 at once)   │
│  • Dims non-constr.   │                           │                       │
└──────────────────────┘                           └───────────────────────┘
        ▲                                                    │
        │              Oracle Cloud VM (1GB RAM)             │
        └────────────── gunicorn + systemd ──────────────────┘
```

---

## ⚡ Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/0xkhush/yt-filter-api.git
cd yt-filter-api

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Fetch real YouTube training data (requires API keys)
python3 fetch_real_data.py

# 5. Train the model
python3 train_model.py

# 6. Start the server
python3 server.py
```

Server starts at `http://localhost:8080`

---

## 📡 API Endpoints

### `POST /predict`

Classify a single YouTube video.

**Request:**
```json
{
  "channel": "3Blue1Brown",
  "title": "Linear Algebra Explained Visually",
  "description": "A visual guide to understanding linear transformations and matrices."
}
```

**Response:**
```json
{
  "constructive": true,
  "confidence": 0.9999,
  "message": "yes"
}
```

| Field | Type | Description |
|---|---|---|
| `channel` | string | YouTube channel name (optional but improves accuracy) |
| `title` | string | Video title (**required** — at least title or description) |
| `description` | string | Video description (**required** — at least title or description) |

---

### `POST /predict/batch`

Classify up to 50 videos in a single request. Used by the feed pre-scanner for instant classification of all visible thumbnails.

**Request:**
```json
{
  "videos": [
    { "channel": "3Blue1Brown", "title": "Linear Algebra" },
    { "channel": "MrBeast", "title": "24 Hour Challenge" }
  ]
}
```

**Response:**
```json
{
  "results": [
    { "constructive": true, "confidence": 0.94 },
    { "constructive": false, "confidence": 0.91 }
  ]
}
```

---

### `GET /health`

Health check endpoint.

```json
{ "status": "ok", "model_loaded": true }
```

---

## 🧠 ML Model Details

### Algorithm

**TF-IDF (Trigrams, 50K features) + Engineered Features → Logistic Regression**

| Component | Details |
|---|---|
| **Vectorizer** | TF-IDF with unigrams, bigrams, and trigrams (50,000 features) |
| **Engineered Features** | 8 hand-crafted signals (caps ratio, !, ?, text length, emoji count, word count, avg word length, ALL CAPS words) |
| **Classifier** | Logistic Regression (C=10, liblinear solver, balanced class weights) |
| **Total Features** | 50,008 |
| **Training Data** | 9,000+ real YouTube videos (API-fetched & Selenium-scraped) |
| **Test Accuracy** | **99.4%** on held-out test set (1,792 samples) |
| **Precision** | 0.993 |
| **Recall** | 0.996 |
| **F1 Score** | 0.9945 |
| **Model Size** | ~28 MB total |

### Performance Metrics

```
              precision    recall  f1-score   support

Non-constructive       0.99      0.99      0.99       793
    Constructive       0.99      1.00      0.99       999

        accuracy                           0.99      1792
```

**Confusion Matrix:** TN=786, FP=7, FN=4, TP=995

### Why This Stack?

- ✅ **Low memory** — runs comfortably on 1GB RAM (~200 MB total)
- ✅ **Fast inference** — single predictions in <10ms, batch of 50 in <50ms
- ✅ **No GPU needed** — pure CPU, no heavy dependencies
- ✅ **Easy to deploy** — just Python + pip, no Docker required
- ✅ **Real data** — trained on 9,000+ actual YouTube videos, not synthetic data
- ✅ **Batch endpoint** — classify 50 videos in a single HTTP request

### Engineered Features

These hand-crafted features capture **stylistic signals** that pure bag-of-words misses:

| Feature | Why It Helps |
|---|---|
| `caps_ratio` | Clickbait/pranks use MUCH more CAPS |
| `exclamation_count` | Non-constructive content abuses exclamations!!! |
| `question_count` | "You won't BELIEVE????" vs calm educational tone |
| `text_length` | Educational descriptions tend to be longer |
| `emoji_count` | Vlogs/pranks use many emojis 😱🔥💀 |
| `word_count` | More words = usually more substantive content |
| `avg_word_len` | Educational content has longer, technical words |
| `all_caps_words` | GONE WRONG, INSANE, BROKEN = non-constructive |

---

## 📊 Data Pipeline

### Real Data Collection

The training data is collected from **real YouTube videos** via the YouTube Data API v3:

#### YouTube Data API v3 Fetcher (`fetch_real_data.py`)

- Uses **multi-key rotation** (3 API keys, 30K units total)
- Fetches video metadata: title, channel, description, category
- **80+ search queries** across educational and non-constructive categories
- **Incremental saving** — data is saved after each category, zero data loss on crash
- Auto-rotates to next key when one hits 403 quota limit

```bash
# Add your API keys to fetch_real_data.py, then:
python3 fetch_real_data.py
```

### Training Data Categories

| Label | Category | Examples |
|---|---|---|
| ✅ `1` | **Education** | Khan Academy, 3Blue1Brown, MIT OCW, CrashCourse |
| ✅ `1` | **Music** | Lofi Girl, Arijit Singh, Classical Music, Orchestras |
| ✅ `1` | **News** | BBC, NDTV, Reuters, Bloomberg, CNN |
| ✅ `1` | **Science** | NASA, Kurzgesagt, Veritasium, NileRed |
| ✅ `1` | **Technology** | Fireship, NetworkChuck, Computerphile |
| ❌ `0` | **Entertainment/Vlogs** | MrBeast, PewDiePie, David Dobrik, CarryMinati |
| ❌ `0` | **Gaming** | Techno Gamerz, Ninja, Dream, xQc |
| ❌ `0` | **Pranks/Drama** | Drama Alert, NELK, Stokes Twins |
| ❌ `0` | **Clickbait/Gossip** | Bright Side, TMZ, 5-Minute Crafts |

---

## 📁 Project Structure

```
yt-filter-api/
├── README.md                 # You're here
├── requirements.txt          # Python dependencies
├── server.py                 # Flask API server (/predict, /predict/batch, /health)
├── train_model.py            # Trains TF-IDF + LogReg on real data
├── fetch_real_data.py        # YouTube API v3 fetcher (multi-key rotation)
├── generate_data.py          # Legacy synthetic data generator (deprecated)
├── data/
│   ├── real_training_data.csv    # Real YouTube data (9,000+ videos, ~14 MB)
│   └── fetched_video_ids.json    # Tracks API-fetched IDs (dedup)
└── model/
    ├── vectorizer.pkl        # TF-IDF vectorizer (~28 MB)
    ├── classifier.pkl        # Logistic Regression model (~0.4 MB)
    └── scaler.pkl            # Feature scaler (~0.001 MB)
```

---

## 🚀 Deploy on Oracle VM (1GB RAM)

### Step 1: Server Setup

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv -y
```

### Step 2: Upload & Configure

```bash
cd /home/ubuntu/yt-filter-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Train Model (One-Time)

```bash
# If you have real data:
python3 train_model.py

# Or upload pre-trained model files:
scp model/*.pkl ubuntu@YOUR_VM_IP:~/yt-filter-api/model/
```

### Step 4: Run with Gunicorn (Production)

```bash
# Single worker, 2 threads — optimized for 1GB RAM
nohup /home/ubuntu/yt-filter-api/venv/bin/gunicorn -w 1 --threads 2 -b 0.0.0.0:8080 server:app > server.log 2>&1 &
```

### Step 5: Systemd Service (Auto-Restart)

```bash
sudo nano /etc/systemd/system/classifier.service
```

```ini
[Unit]
Description=YouTube Content Classifier API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/yt-filter-api
ExecStart=/home/ubuntu/yt-filter-api/venv/bin/gunicorn -w 1 --threads 2 -b 0.0.0.0:8080 server:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable classifier
sudo systemctl start classifier
sudo systemctl status classifier
```

### Step 6: Open Firewall

```bash
# Oracle Cloud — open port 8080 in security list
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8080 -j ACCEPT
sudo netfilter-persistent save
```

### Memory Estimate

| Component | RAM |
|---|---|
| Python + Flask | ~40 MB |
| TF-IDF Vectorizer (50K) | ~120 MB |
| Classifier + Scaler | ~20 MB |
| **Total** | **~200 MB** |

Leaves ~800 MB free for the OS and other services.

---

## 🔌 Browser Extension Integration

### Single Video Classification

```javascript
const response = await fetch('http://YOUR_VM_IP:8080/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ channel, title, description })
});
const data = await response.json();
// { constructive: true/false, confidence: 0.94, message: "yes"/"no" }
```

### Batch Feed Pre-Scan (50 videos at once)

```javascript
const response = await fetch('http://YOUR_VM_IP:8080/predict/batch', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    videos: thumbnails.map(v => ({ channel: v.channel, title: v.title }))
  })
});
const data = await response.json();
// { results: [{ constructive: true, confidence: 0.94 }, ...] }
```

---

## 📦 Dependencies

```
flask==3.1.1          # Web framework
flask-cors==5.0.1     # CORS for browser extension
scikit-learn==1.6.1   # ML (TF-IDF + LogReg)
joblib==1.5.0         # Model serialization
gunicorn==23.0.0      # Production WSGI server
pandas==2.2.3         # Data handling
requests              # YouTube API fetching
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/0xkhush">@0xkhush</a>
</p>
