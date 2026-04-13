"""
fetch_real_data.py — Fetches REAL YouTube video metadata using YouTube Data API v3.
Collects channel name, title, description for training the ML classifier.

Usage:
    python3 fetch_real_data.py

Quota info:
    - YouTube API gives 10,000 units/day PER KEY
    - 3 keys = 30,000 total units
    - Each search costs 100 units, returns up to 50 results
    - Auto-rotates keys when one gets exhausted (403)
    - Saves data IMMEDIATELY after each category — zero data loss

Output:
    data/real_training_data.csv  (appends, never overwrites)
"""

import os
import csv
import json
import time
import requests

# ─── CONFIG ──────────────────────────────────────────────────────────────────
# 3 API keys — auto-rotates when one is exhausted
API_KEYS = [
    "api_key1",
    "api_key2",
    "api_key3",
]
current_key_index = 0

def get_api_key():
    """Get the current active API key."""
    return API_KEYS[current_key_index]

def rotate_key():
    """Switch to the next API key. Returns False if all keys exhausted."""
    global current_key_index
    current_key_index += 1
    if current_key_index >= len(API_KEYS):
        return False
    print(f"\n    🔄 Key {current_key_index} exhausted → switching to key {current_key_index + 1}/{len(API_KEYS)}")
    return True

BASE_URL = "https://www.googleapis.com/youtube/v3"
OUTPUT_FILE = "data/real_training_data.csv"
TRACKER_FILE = "data/fetched_video_ids.json"
MAX_RESULTS = 50  # Max per API call

# ─── CATEGORY SEARCH CONFIGS ────────────────────────────────────────────────
# Each entry: (search_query, youtube_category_id or None, label, category_name)
# YouTube Category IDs: 10=Music, 20=Gaming, 22=People&Blogs, 24=Entertainment,
#                       25=News, 27=Education, 28=Science&Technology

SEARCH_CONFIGS = {
    # ═══════════════════════════════════════════════════════════════════════
    # CONSTRUCTIVE (label=1)
    # ═══════════════════════════════════════════════════════════════════════
    "Education": {
        "label": 1,
        "category_id": "27",
        "queries": [
            "python tutorial for beginners",
            "java programming course",
            "javascript tutorial",
            "data structures and algorithms",
            "machine learning full course",
            "deep learning tutorial",
            "web development course",
            "react js tutorial",
            "node js tutorial for beginners",
            "sql tutorial for beginners",
            "power bi tutorial",
            "DAX tutorial power bi",
            "tableau tutorial for beginners",
            "excel tutorial advanced",
            "data analytics course",
            "cloud computing tutorial",
            "docker kubernetes tutorial",
            "system design interview",
            "operating system lecture",
            "computer networks lecture",
            "GATE preparation computer science",
            "JEE physics lecture",
            "NEET biology lecture",
            "calculus lecture university",
            "linear algebra full course",
            "statistics for data science",
            "cybersecurity tutorial",
            "ethical hacking course",
            "flutter tutorial",
            "android development tutorial",
            "DSA interview preparation",
            "competitive programming tutorial",
            "C++ STL tutorial",
            "django tutorial for beginners",
            "flask python tutorial",
            "AWS tutorial for beginners",
            "git github tutorial",
            "artificial intelligence course",
            "NLP natural language processing",
            "computer vision tutorial",
        ],
    },
    "Music": {
        "label": 1,
        "category_id": "10",
        "queries": [
            "classical music playlist",
            "lofi hip hop study music",
            "piano music relaxing",
            "guitar tutorial beginners",
            "bollywood songs playlist",
            "jazz music collection",
            "acoustic covers popular songs",
            "music theory lesson",
            "singing tutorial",
            "drum tutorial beginners",
            "symphony orchestra performance",
            "arijit singh songs collection",
            "ar rahman hits",
            "indie music playlist",
            "ambient music for focus",
            "sitar classical music",
            "blues guitar lessons",
            "music production tutorial",
            "beatmaking tutorial",
            "violin tutorial for beginners",
            "devotional songs collection",
            "sufi music best",
            "carnatic music concert",
            "rock classics playlist",
            "EDM mix playlist",
        ],
    },
    "News": {
        "label": 1,
        "category_id": "25",
        "queries": [
            "world news today",
            "breaking news analysis",
            "geopolitics explained",
            "economic news analysis",
            "india news today",
            "technology news update",
            "climate change news",
            "international relations analysis",
            "stock market analysis today",
            "political analysis",
            "investigative journalism documentary",
            "business news update",
            "foreign policy analysis",
            "defense news update",
            "science news latest discoveries",
            "UN general assembly",
            "G20 summit coverage",
            "election analysis",
            "budget analysis explained",
            "trade war explained",
        ],
    },
    "Science": {
        "label": 1,
        "category_id": "28",
        "queries": [
            "space documentary",
            "quantum physics explained",
            "black holes explained",
            "chemistry experiments",
            "biology documentary",
            "mars exploration NASA",
            "james webb telescope discoveries",
            "climate science explained",
            "medical science documentary",
            "neuroscience explained",
            "engineering explained",
            "how things work science",
            "physics experiment demonstration",
            "evolution documentary",
            "ocean exploration documentary",
            "nuclear fusion explained",
            "astronomy for beginners",
            "scientific discoveries 2024",
            "nanotechnology explained",
            "genetics and DNA explained",
        ],
    },

    # ═══════════════════════════════════════════════════════════════════════
    # NON-CONSTRUCTIVE (label=0)
    # ═══════════════════════════════════════════════════════════════════════
    "Entertainment": {
        "label": 0,
        "category_id": "24",
        "queries": [
            "vlog day in my life",
            "24 hour challenge",
            "unboxing haul shopping",
            "room tour mansion",
            "morning routine 2024",
            "get ready with me",
            "try not to laugh challenge",
            "mukbang eating challenge",
            "travel vlog luxury",
            "birthday surprise vlog",
            "apartment tour",
            "food challenge extreme",
            "lifestyle vlog daily",
            "shopping spree challenge",
            "what I eat in a day",
            "reaction compilation",
            "storytime animated",
            "subscriber challenge",
            "YouTuber house tour",
            "transformation challenge",
            "blind date challenge",
            "extreme dare challenge",
            "speed dating challenge",
            "outfit rating challenge",
            "mystery box challenge",
        ],
    },
    "Gaming": {
        "label": 0,
        "category_id": "20",
        "queries": [
            "minecraft but challenge",
            "fortnite gameplay highlights",
            "GTA 5 funny moments",
            "valorant ranked gameplay",
            "pubg mobile gameplay",
            "free fire gameplay",
            "roblox gameplay",
            "among us funny moments",
            "gaming rage compilation",
            "call of duty gameplay",
            "apex legends montage",
            "league of legends gameplay",
            "elden ring boss fight",
            "speedrun world record",
            "gaming setup tour",
            "pro vs noob gaming",
            "trolling in games",
            "first time playing game",
            "gaming clips compilation",
            "live stream gaming highlights",
        ],
    },
    "Pranks_Drama": {
        "label": 0,
        "category_id": None,  # Search across categories
        "queries": [
            "prank on girlfriend gone wrong",
            "prank on mom",
            "scary prank compilation",
            "exposing youtuber drama",
            "youtuber controversy explained",
            "cancel culture drama",
            "roasting youtubers",
            "3am challenge scary",
            "truth or dare extreme",
            "hidden camera prank",
            "public prank reactions",
            "girlfriend prank",
            "breakup prank emotional",
            "ouija board challenge",
            "internet drama breakdown",
            "youtuber beef explained",
            "celebrity drama tea",
            "revenge prank",
            "spying on partner prank",
            "destroying property prank",
        ],
    },
    "Clickbait_Gossip": {
        "label": 0,
        "category_id": None,
        "queries": [
            "celebrity gossip news",
            "things you didn't know about",
            "most expensive things owned by",
            "shocking celebrity facts",
            "life hacks you need to know",
            "facts that will blow your mind",
            "top 10 most amazing",
            "you won't believe what happened",
            "richest celebrities net worth",
            "celebrities without makeup",
            "celebrity couple breakup",
            "bollywood gossip latest",
            "hollywood gossip news",
            "5 minute crafts life hacks",
            "mystery stories scary",
            "unsolved mysteries creepy",
            "celebrity transformation shocking",
            "things you've been doing wrong",
            "dark secrets of celebrities",
            "most expensive things in the world",
        ],
    },
}


# ─── API FUNCTIONS ───────────────────────────────────────────────────────────

def search_videos(query, category_id=None, max_results=50):
    """Search YouTube for videos. Auto-rotates API key on 403."""
    while True:
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "key": get_api_key(),
            "relevanceLanguage": "en",
            "order": "relevance",
        }
        if category_id:
            params["videoCategoryId"] = category_id

        try:
            resp = requests.get(f"{BASE_URL}/search", params=params, timeout=15)
            if resp.status_code == 403:
                # Quota exhausted — try next key
                if not rotate_key():
                    print("    ❌ ALL API KEYS EXHAUSTED")
                    return None  # Signal all keys dead
                continue  # Retry with new key
            resp.raise_for_status()
            data = resp.json()

            video_ids = []
            for item in data.get("items", []):
                vid_id = item.get("id", {}).get("videoId")
                if vid_id:
                    video_ids.append(vid_id)
            return video_ids
        except requests.exceptions.HTTPError:
            if not rotate_key():
                return None
            continue
        except Exception as e:
            print(f"    ⚠️  Search error: {e}")
            return []


def get_video_details(video_ids):
    """Fetch detailed info for a batch of video IDs. Auto-rotates key on 403."""
    results = []

    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]

        while True:
            params = {
                "part": "snippet",
                "id": ",".join(batch),
                "key": get_api_key(),
            }

            try:
                resp = requests.get(f"{BASE_URL}/videos", params=params, timeout=15)
                if resp.status_code == 403:
                    if not rotate_key():
                        return results  # Return what we have so far
                    continue
                resp.raise_for_status()
                data = resp.json()

                for item in data.get("items", []):
                    snippet = item.get("snippet", {})
                    results.append({
                        "video_id": item["id"],
                        "channel_name": snippet.get("channelTitle", ""),
                        "title": snippet.get("title", ""),
                        "description": snippet.get("description", ""),
                    })
                break  # Success — move to next batch
            except requests.exceptions.HTTPError:
                if not rotate_key():
                    return results
                continue
            except Exception as e:
                print(f"    ⚠️  Details error: {e}")
                break

        time.sleep(0.2)

    return results


# ─── MAIN ────────────────────────────────────────────────────────────────────

def load_existing_ids():
    """Load previously fetched video IDs to avoid duplicates."""
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_ids(ids_set):
    """Save fetched video IDs."""
    with open(TRACKER_FILE, "w") as f:
        json.dump(list(ids_set), f)


def save_samples_to_csv(samples):
    """Incrementally save samples to CSV (append mode, never lose data)."""
    if not samples:
        return
    
    file_exists = os.path.exists(OUTPUT_FILE)
    fieldnames = ["channel_name", "title", "description", "label", "category", "video_id"]
    
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        
        for sample in samples:
            sample["description"] = str(sample.get("description", "")).replace("\n", " ").replace("\r", " ").strip()
            # Only write the fields we need
            row = {k: sample.get(k, "") for k in fieldnames}
            writer.writerow(row)


def main():
    os.makedirs("data", exist_ok=True)
    
    existing_ids = load_existing_ids()
    print(f"🔑 Using {len(API_KEYS)} API keys ({len(API_KEYS) * 10000} total units)\n")

    total_new = 0
    total_constructive = 0
    total_non_constructive = 0
    all_keys_dead = False
    
    for category_name, config in SEARCH_CONFIGS.items():
        if all_keys_dead:
            print(f"⚠️  Skipping {category_name} — ALL API keys exhausted")
            continue
        
        label = config["label"]
        cat_id = config["category_id"]
        queries = config["queries"]
        icon = "✅" if label == 1 else "❌"
        
        print(f"{icon} Fetching: {category_name} (label={label})")
        
        category_videos = []
        
        for i, query in enumerate(queries):
            print(f"    [{i+1}/{len(queries)}] Searching: \"{query}\"", end="")
            
            # Search for video IDs
            video_ids = search_videos(query, cat_id)
            
            # None means ALL keys exhausted
            if video_ids is None:
                print(" → ALL KEYS EXHAUSTED")
                all_keys_dead = True
                break
            
            # Filter out already-fetched
            new_ids = [vid for vid in video_ids if vid not in existing_ids]
            
            if not new_ids:
                print(f" → 0 new (all duplicates)")
                continue
            
            # Fetch details for new videos
            details = get_video_details(new_ids)
            
            # Add to collection
            for vid in details:
                vid["label"] = label
                vid["category"] = category_name
                category_videos.append(vid)
                existing_ids.add(vid["video_id"])
            
            print(f" → {len(details)} new videos")
            time.sleep(0.3)
        
        # ── SAVE IMMEDIATELY after each category ─────────────────────────────
        if category_videos:
            save_samples_to_csv(category_videos)
            save_ids(existing_ids)
            cat_count = len(category_videos)
            total_new += cat_count
            if label == 1:
                total_constructive += cat_count
            else:
                total_non_constructive += cat_count
            print(f"    💾 Saved {cat_count} videos for {category_name}\n")
        else:
            print(f"    Total for {category_name}: 0\n")
    
    # ── Final Stats ──────────────────────────────────────────────────────────
    print("=" * 55)
    print("📊 FETCH RESULTS")
    print("=" * 55)
    print(f"  New videos fetched:   {total_new}")
    print(f"  Constructive (1):     {total_constructive}")
    print(f"  Non-constructive (0): {total_non_constructive}")
    print(f"  Total in database:    {len(existing_ids)}")
    print(f"  Keys used:            {current_key_index + 1}/{len(API_KEYS)}")
    print(f"\n  Saved to: {OUTPUT_FILE}")
    if all_keys_dead:
        print(f"  ⚠️  All keys exhausted! Add more keys or run again tomorrow.")
    else:
        print(f"  ✅ Done! Run again to fetch more.")


if __name__ == "__main__":
    main()
