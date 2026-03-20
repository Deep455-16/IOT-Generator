from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env (for local testing)
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# =========================
# MongoDB Connection (Atlas) with forced TLS
# =========================
MONGO_URI = os.environ.get("MONGO_URI")  # e.g., mongodb+srv://user:pass@cluster0.vpferkw.mongodb.net/iot_db?retryWrites=true&w=majority

client = None
collection = None

try:
    if MONGO_URI:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            tls=True,  # Force TLS
            tlsAllowInvalidCertificates=False  # Atlas requires valid certificates
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