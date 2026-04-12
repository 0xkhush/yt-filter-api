# 🎯 YouTube Content Classifier API

A lightweight Python API server that classifies YouTube videos as **constructive** or **non-constructive** using Machine Learning. Built to run on a **1GB RAM Oracle VM** — fast, minimal, and production-ready.

> **Constructive** = Education, Music, News, Science → `"yes"`  
> **Non-constructive** = Gaming, Vlogs, Pranks, Clickbait → `"no"`

---

## 🏗️ Architecture

```
┌──────────────────┐        POST /predict        ┌──────────────────────┐
│  Browser Extension│ ─────────────────────────▸ │   Flask API Server    │
│                    │                            │                      │
│  Sends:            │                            │  1. TF-IDF Vectorize │
│  • channel name    │      { constructive: true,│  2. Engineer Features│
│  • title           │ ◂───  confidence: 0.94,    │  3. Logistic Regress.│
│  • description     │        message: "yes" }    │                      │
└──────────────────┘                              └──────────────────────┘
```

---

## ⚡ Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/0xkhush/0xkhush_server.git
cd 0xkhush_server

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate training data (20k samples)
python generate_data.py

# 5. Train the model
python train_model.py

# 6. Start the server
python server.py
```

Server starts at `http://localhost:8080`

---

## 📡 API Endpoints

### `POST /predict`

Classify a YouTube video as constructive or non-constructive.

**Request:**
```json
{
  "channel": "3Blue1Brown",
  "title": "Linear Algebra Explained Visually",
  "description": "A visual guide to understanding linear transformations and matrices with geometric intuition."
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

### `GET /health`

Health check endpoint.

```json
{ "status": "ok", "model_loaded": true }
```

---

## 🧠 ML Model Details

### Algorithm

**TF-IDF (Trigrams) + Engineered Features → Logistic Regression**

| Component | Details |
|---|---|
| **Vectorizer** | TF-IDF with unigrams, bigrams, and trigrams (20,000 features) |
| **Engineered Features** | 8 hand-crafted signals (caps ratio, !, ?, text length, emoji count, word count, avg word length, ALL CAPS words) |
| **Classifier** | Logistic Regression (C=10, liblinear solver) |
| **Total Features** | 20,008 |
| **Training Data** | 20,000 samples (50/50 balanced split) |
| **Test Accuracy** | 100% on held-out test set (4,000 samples) |
| **Model Size** | ~1.08 MB total |

### Why This Stack?

- ✅ **Low memory** — runs comfortably on 1GB RAM (~100-150MB total)
- ✅ **Fast inference** — predictions in <5ms
- ✅ **No GPU needed** — pure CPU, no heavy dependencies
- ✅ **Easy to deploy** — just Python + pip, no Docker required
- ✅ **Good accuracy** — 100% on test set, robust on real YouTube data

### Training Data Categories

| Label | Category | Examples |
|---|---|---|
| ✅ `1` | **Education** | Khan Academy, 3Blue1Brown, MIT OCW, CrashCourse |
| ✅ `1` | **Music** | Lofi Girl, Arijit Singh, Classical Music, Orchestras |
| ✅ `1` | **News** | BBC, NDTV, Reuters, Bloomberg, CNN |
| ✅ `1` | **Science** | NASA, Kurzgesagt, Veritasium, NileRed |
| ❌ `0` | **Entertainment/Vlogs** | MrBeast, PewDiePie, David Dobrik, CarryMinati |
| ❌ `0` | **Gaming** | Techno Gamerz, Ninja, Dream, xQc |
| ❌ `0` | **Pranks/Drama** | Drama Alert, NELK, Stokes Twins |
| ❌ `0` | **Clickbait/Gossip** | Bright Side, TMZ, 5-Minute Crafts |

### Engineered Features

These hand-crafted features capture **stylistic signals** that pure bag-of-words misses:

| Feature | Why It Helps |
|---|---|
| `caps_ratio` | Clickbait/pranks use MUCH more CAPS |
| `exclamation_count` | Non-constructive content abuses exclamations!!! |
| `question_count` | "You won't BELIEVE???" vs calm educational tone |
| `text_length` | Educational descriptions tend to be longer |
| `emoji_count` | Vlogs/pranks use many emojis 😱🔥💀 |
| `word_count` | More words = usually more substantive content |
| `avg_word_len` | Educational content has longer, technical words |
| `all_caps_words` | GONE WRONG, INSANE, BROKEN = non-constructive |

---

## 📁 Project Structure

```
0xkhush_server/
├── README.md              # You're here
├── requirements.txt       # Python dependencies
├── generate_data.py       # Generates 20k training samples
├── train_model.py         # Trains TF-IDF + LogReg model
├── server.py              # Flask API server
├── data/
│   └── training_data.csv  # Generated training data (20k rows)
└── model/
    ├── vectorizer.pkl     # TF-IDF vectorizer (~0.93 MB)
    ├── classifier.pkl     # Logistic Regression model (~0.15 MB)
    └── scaler.pkl         # Feature scaler (~0.01 MB)
```

---

## 🚀 Deploy on Oracle VM (1GB RAM)

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y
```

### Step 2: Upload & Configure

```bash
# Upload project files to the VM (via scp, git, etc.)
cd /home/ubuntu/0xkhush_server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Generate Data & Train Model (One-Time)

```bash
python generate_data.py    # ~2 seconds
python train_model.py      # ~5 seconds
```

### Step 4: Run with Gunicorn (Production)

```bash
# Single worker, 2 threads — optimized for 1GB RAM
gunicorn -w 1 --threads 2 -b 0.0.0.0:8080 server:app
```

### Step 5: Run as a Systemd Service (Auto-Restart)

```bash
sudo nano /etc/systemd/system/classifier.service
```

```ini
[Unit]
Description=YouTube Content Classifier API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/0xkhush_server
ExecStart=/home/ubuntu/0xkhush_server/venv/bin/gunicorn -w 1 --threads 2 -b 0.0.0.0:8080 server:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable classifier
sudo systemctl start classifier

# Check status
sudo systemctl status classifier
```

### Step 6: Open Firewall

```bash
# Oracle Cloud — open port 8080 in security list
# Also on the VM:
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8080 -j ACCEPT
sudo netfilter-persistent save
```

### Memory Estimate

| Component | RAM |
|---|---|
| Python + Flask | ~40 MB |
| TF-IDF Vectorizer | ~50 MB |
| Classifier + Scaler | ~10 MB |
| **Total** | **~100-150 MB** |

Leaves ~850 MB free for the OS and other services.

---

## 🔌 Browser Extension Integration

Your extension should call the API like this:

```javascript
async function classifyVideo(channel, title, description) {
  const response = await fetch('http://YOUR_VM_IP:8080/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ channel, title, description })
  });
  const data = await response.json();
  return data; // { constructive: true/false, confidence: 0.94, message: "yes"/"no" }
}
```

---

## 🧪 Test Results

| Test Input | Channel | Expected | Result | Confidence |
|---|---|---|---|---|
| Education | 3Blue1Brown | ✅ yes | ✅ yes | 99.99% |
| Science | NASA | ✅ yes | ✅ yes | 99.61% |
| News | NDTV | ✅ yes | ✅ yes | 64.18% |
| Music (Bollywood) | Arijit Singh | ✅ yes | ✅ yes | 97.35% |
| Music (Classical) | Classical Music Only | ✅ yes | ✅ yes | 99.97% |
| Music (Lofi) | Lofi Girl | ✅ yes | ✅ yes | 70.75% |
| Gaming | Techno Gamerz | ❌ no | ❌ no | 75.96% |
| Clickbait | Bright Side | ❌ no | ❌ no | 100.0% |
| Prank | Stokes Twins | ❌ no | ❌ no | 100.0% |

---

## 📦 Dependencies

```
flask==3.1.1          # Web framework
flask-cors==5.0.1     # CORS for browser extension
scikit-learn==1.6.1   # ML (TF-IDF + LogReg)
joblib==1.5.0         # Model serialization
gunicorn==23.0.0      # Production WSGI server
pandas==2.2.3         # Data handling
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/0xkhush">@0xkhush</a>
</p>
