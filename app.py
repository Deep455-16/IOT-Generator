from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import os
import certifi
from dotenv import load_dotenv

# ─── Monkey-patch pymongo's SSL context factory ───────────────────────────────
import pymongo.ssl_support as _pymongo_ssl

_orig_get_ssl_context = _pymongo_ssl.get_ssl_context

def _patched_get_ssl_context(*args, **kwargs):
    ctx = _orig_get_ssl_context(*args, **kwargs)
    try:
        ctx.set_ciphers("DEFAULT:@SECLEVEL=1")
    except Exception:
        pass
    return ctx

_pymongo_ssl.get_ssl_context = _patched_get_ssl_context
import pymongo.client_options as _pymongo_co
_pymongo_co.get_ssl_context = _patched_get_ssl_context
# ─────────────────────────────────────────────────────────────────────────────

from pymongo import MongoClient

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')

# ✅ FIXED: Explicit CORS — allows all origins, all methods, all headers
#    Simple CORS(app) sometimes fails on Render because it doesn't set
#    the correct headers for preflight OPTIONS requests.
CORS(app,
     resources={r"/api/*": {"origins": "*"}},
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"],
     supports_credentials=False)

# ✅ FIXED: Handle OPTIONS preflight requests explicitly
#    Browsers send an OPTIONS request before POST — if this isn't handled,
#    the actual POST never gets made and fetch() throws a network error.
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = app.make_default_options_response()
        res.headers["Access-Control-Allow-Origin"]  = "*"
        res.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        res.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return res

# =========================
# MongoDB Connection (Atlas)
# =========================
MONGO_URI = os.environ.get("MONGO_URI")

client     = None
collection = None

try:
    if MONGO_URI:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            tls=True,
            tlsCAFile=certifi.where(),
        )
        db         = client["iot_db"]
        collection = db["projects"]
        client.server_info()
        print("✅ MongoDB connected successfully")
    else:
        print("⚠️ MONGO_URI environment variable not found")
except Exception as e:
    print("❌ MongoDB connection error:", e)
    import traceback
    traceback.print_exc()

# =========================
# Load projects.json as local fallback
# =========================
import json

_JSON_PROJECTS = []
_JSON_PATH     = os.path.join(os.path.dirname(__file__), "projects.json")

try:
    with open(_JSON_PATH, "r") as _f:
        _JSON_PROJECTS = json.load(_f)
    print(f"✅ projects.json loaded ({len(_JSON_PROJECTS)} projects)")
except Exception as _e:
    print(f"⚠️  projects.json not found or invalid: {_e}")


def _json_find_one(category: str, difficulty: str, topic: str = ""):
    topic_lower = topic.lower()
    if topic_lower:
        for p in _JSON_PROJECTS:
            if (p.get("category") == category
                    and p.get("difficulty") == difficulty
                    and topic_lower in p.get("title", "").lower()):
                return p
    matches = [
        p for p in _JSON_PROJECTS
        if p.get("category") == category and p.get("difficulty") == difficulty
    ]
    return random.choice(matches) if matches else None


def _json_find_ideas(category: str, difficulty: str, limit: int = 4):
    matches = [
        p for p in _JSON_PROJECTS
        if p.get("category") == category and p.get("difficulty") == difficulty
    ]
    sample = random.sample(matches, min(limit, len(matches))) if matches else []
    return [
        {
            "title":       p.get("title", ""),
            "overview":    p.get("overview", ""),
            "description": p.get("description", p.get("overview", ""))[:120] + "...",
            "wow_factor":  p.get("wow_factor", "Cool IoT project!"),
            "components":  [c.get("name", c) if isinstance(c, dict) else c
                            for c in p.get("components", [])[:3]],
        }
        for p in sample
    ]


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
    """Last-resort fallback if both MongoDB and projects.json fail"""
    project = {
        "title":          _format_title(topic, category),
        "tagline":        f"A {difficulty.lower()} {category.lower()} project.",
        "overview":       f"This project helps build a {topic.lower()} system.",
        "difficulty":     difficulty,
        "category":       category,
        "estimated_time": "3-5 hours",
        "estimated_cost": "$30 - $60",
        "cost_range":     "$30 - $60",
        "time_estimate":  "3-5 hours",
        "cost":           "$30 - $60",
        "components": [
            {"name": "ESP32",  "quantity": 1, "purpose": "Main controller",  "approximate_cost": "$8"},
            {"name": "Sensor", "quantity": 1, "purpose": "Data input",       "approximate_cost": "$5"},
            {"name": "Relay",  "quantity": 1, "purpose": "Actuator control", "approximate_cost": "$3"},
        ],
        "architecture": {
            "layers": [
                {"name": "Perception Layer",  "description": "Sensors collect real-world data"},
                {"name": "Network Layer",     "description": "Wi-Fi transmits data to broker"},
                {"name": "Application Layer", "description": "Dashboard visualises data"},
            ]
        },
        "steps": [
            {"step_number": 1, "title": "Gather Components", "description": "Purchase all hardware components.", "duration": "", "code_snippet": "", "tips": []},
            {"step_number": 2, "title": "Circuit Assembly",  "description": "Connect components on breadboard.", "duration": "", "code_snippet": "", "tips": []},
            {"step_number": 3, "title": "Upload Firmware",   "description": "Flash the microcontroller code.",   "duration": "", "code_snippet": "", "tips": []},
            {"step_number": 4, "title": "Test & Deploy",     "description": "Verify readings and go live.",      "duration": "", "code_snippet": "", "tips": []},
        ],
        "code": {
            "language":    "Python",
            "main_code":   "# Sample Code\nprint('IoT project running')",
            "explanation": "Basic template code for the project."
        },
        "testing": {
            "steps":           ["Power on and verify sensor readings", "Check MQTT messages in broker"],
            "expected_output": "Sensor returns stable readings. MQTT publishes data every 5 seconds."
        },
        "troubleshooting": [
            {"problem": "Sensor reads 0",       "solution": "Check wiring and power supply"},
            {"problem": "Wi-Fi not connecting", "solution": "Verify SSID and password in code"},
        ],
        "extensions":  ["Add mobile app", "Integrate with cloud dashboard"],
        "description": f"A {difficulty.lower()} IoT project: {topic}",
        "wow_factor":  "Build real IoT skills with hands-on hardware!",
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
    return jsonify({
        'message':       'Backend is working',
        'mongodb':       collection is not None,
        'json_projects': len(_JSON_PROJECTS),
        'port':          os.environ.get("PORT", "5000 (local default)"),
    })


@app.route('/api/generate', methods=['POST'])
def generate_project():
    data       = request.get_json() or {}
    topic      = data.get('topic', '').strip()
    difficulty = data.get('difficulty', 'Beginner')
    category   = data.get('category', 'Home Automation')

    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    try:
        # ── MongoDB first ──────────────────────────────────────────────────
        if collection is not None:
            # Use $sample so a different project is returned each time
            pipeline = [
                {"$match": {
                    "category":   category,
                    "difficulty": difficulty,
                    "title":      {"$regex": topic, "$options": "i"}
                }},
                {"$sample": {"size": 1}}
            ]
            result = list(collection.aggregate(pipeline))

            # Fallback: any project with same category + difficulty
            if not result:
                pipeline = [
                    {"$match": {"category": category, "difficulty": difficulty}},
                    {"$sample": {"size": 1}}
                ]
                result = list(collection.aggregate(pipeline))

            if result:
                project        = result[0]
                project["_id"] = str(project["_id"])
                return jsonify({'success': True, 'project': project})

        # ── projects.json fallback ─────────────────────────────────────────
        json_project = _json_find_one(category, difficulty, topic)
        if json_project:
            return jsonify({'success': True, 'project': json_project})

        # ── Last resort ────────────────────────────────────────────────────
        return jsonify({'success': True,
                        'project': _build_project(topic, difficulty, category)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/quick-ideas', methods=['POST'])
def quick_ideas():
    data       = request.get_json() or {}
    category   = data.get('category', 'Home Automation')
    difficulty = data.get('difficulty', 'Beginner')

    try:
        if collection is not None:
            # Use $sample for variety + return all fields quick-ideas needs
            pipeline = [
                {"$match": {"category": category, "difficulty": difficulty}},
                {"$sample": {"size": 4}},
                {"$project": {
                    "title":       1,
                    "overview":    1,
                    "description": 1,
                    "wow_factor":  1,
                    "components":  1,
                }}
            ]
            ideas = list(collection.aggregate(pipeline))
            if ideas:
                for idea in ideas:
                    idea["_id"] = str(idea["_id"])
                    if not idea.get("description"):
                        idea["description"] = idea.get("overview", "")[:120] + "..."
                    if not idea.get("wow_factor"):
                        idea["wow_factor"] = "Cool IoT project!"
                    raw = idea.get("components", [])
                    idea["components"] = [
                        c.get("name", c) if isinstance(c, dict) else c
                        for c in raw[:3]
                    ]
                return jsonify({'success': True, 'ideas': ideas})

        # ── projects.json fallback ─────────────────────────────────────────
        json_ideas = _json_find_ideas(category, difficulty, limit=4)
        if json_ideas:
            return jsonify({'success': True, 'ideas': json_ideas})

        # ── Last resort ────────────────────────────────────────────────────
        return jsonify({'success': True, 'ideas': [{
            "title":       "Smart Plant Watering System",
            "description": "Auto-water your plants based on soil moisture",
            "components":  ["ESP32", "Soil Sensor", "Water Pump"],
            "wow_factor":  "Never let a plant die again!"
        }]})

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
    # Render sets PORT env var to 10000 automatically.
    # Locally it falls back to 5000.
    # Both cases handled by this single line.
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting Flask on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
