from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import os
import certifi
from dotenv import load_dotenv

# ─── Monkey-patch pymongo's SSL context factory ─────────────────────────────
# Python 3.14 ships OpenSSL 3.6+ which defaults to SECLEVEL=2. MongoDB Atlas
# rejects the handshake at that level (TLSV1_ALERT_INTERNAL_ERROR).  We wrap
# pymongo's internal get_ssl_context() so every SSLContext it creates gets
# SECLEVEL lowered to 1 before pymongo uses it.
# This MUST run before importing MongoClient so the wrapped version is in place.
import pymongo.ssl_support as _pymongo_ssl

_orig_get_ssl_context = _pymongo_ssl.get_ssl_context

def _patched_get_ssl_context(*args, **kwargs):
    ctx = _orig_get_ssl_context(*args, **kwargs)
    try:
        ctx.set_ciphers("DEFAULT:@SECLEVEL=1")
    except Exception:
        pass  # Older OpenSSL without @SECLEVEL support; safe to ignore
    return ctx

_pymongo_ssl.get_ssl_context = _patched_get_ssl_context
# Also patch the reference already imported in client_options
import pymongo.client_options as _pymongo_co
_pymongo_co.get_ssl_context = _patched_get_ssl_context
# ─────────────────────────────────────────────────────────────────────────────

from pymongo import MongoClient

# Load environment variables from .env (for local testing)
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# =========================
# MongoDB Connection (Atlas)
# =========================
MONGO_URI = os.environ.get("MONGO_URI")

client = None
collection = None

try:
    if MONGO_URI:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            tls=True,
            tlsCAFile=certifi.where(),
        )
        db = client["iot_db"]
        collection = db["projects"]
        # Quick test to ensure connection works
        client.server_info()
        print("✅ MongoDB connected successfully")
    else:
        print("⚠️ MONGO_URI environment variable not found")
except Exception as e:
    print("❌ MongoDB connection error:", e)
    import traceback
    traceback.print_exc()

# =========================
# Utility Functions
# =========================
def _seeded_random(topic: str, difficulty: str, category: str):
    seed = f"{topic}|{difficulty}|{category}"
    return random.Random(seed)

def _format_title(topic: str, category: str):
    if topic.lower().startswith("smart"):
        return topic.title()
    return f"Smart {topic.title()} System"

def _build_project(topic: str, difficulty: str, category: str):
    """Fallback generator if MongoDB data not available"""
    rng = _seeded_random(topic, difficulty, category)
    project = {
        "title": _format_title(topic, category),
        "tagline": f"A {difficulty.lower()} {category.lower()} project.",
        "overview": f"This project helps build a {topic.lower()} system.",
        "difficulty": difficulty,
        "category": category,
        "estimated_time": "3-5 hours",
        "estimated_cost": "$30–$60",
        "components": [
            {"name": "ESP32", "quantity": 1, "purpose": "Controller", "approximate_cost": "$8"},
            {"name": "Sensor", "quantity": 1, "purpose": "Input", "approximate_cost": "$5"}
        ],
        "steps": [],
        "code": {
            "language": "Python",
            "main_code": "# Sample Code",
            "explanation": "Basic template"
        }
    }
    return project

# =========================
# Routes
# =========================
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'Backend is working'})

@app.route('/api/generate', methods=['POST'])
def generate_project():
    data = request.get_json() or {}
    topic = data.get('topic', '').strip()
    difficulty = data.get('difficulty', 'Beginner')
    category = data.get('category', 'Home Automation')

    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    try:
        # ✅ MongoDB first
        if collection is not None:
            project = collection.find_one({"category": category, "difficulty": difficulty})
            if project:
                project["_id"] = str(project["_id"])
                return jsonify({'success': True, 'project': project})

        # 🔥 Fallback if DB empty
        project_data = _build_project(topic, difficulty, category)
        return jsonify({'success': True, 'project': project_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quick-ideas', methods=['POST'])
def quick_ideas():
    data = request.get_json() or {}
    category = data.get('category', 'Home Automation')
    difficulty = data.get('difficulty', 'Beginner')

    try:
        if collection is not None:
            ideas = list(collection.find(
                {"category": category, "difficulty": difficulty},
                {"title": 1, "overview": 1}
            ).limit(4))
            if ideas:
                for idea in ideas:
                    idea["_id"] = str(idea["_id"])
                return jsonify({'success': True, 'ideas': ideas})

        # Fallback
        fallback = [
            {"title": "Smart Plant System", "description": "Auto watering system", "components": [], "wow_factor": "Cool IoT"}
        ]
        return jsonify({'success': True, 'ideas': fallback})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save', methods=['POST'])
def save_project():
    data = request.get_json()
    try:
        if collection is not None:
            collection.insert_one(data)
            return jsonify({'success': True})
        return jsonify({'error': 'Database not connected'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =========================
# Run server
# =========================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)