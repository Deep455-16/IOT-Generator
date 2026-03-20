from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
from dotenv import load_dotenv
import certifi

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# =========================
# MongoDB Connection (Atlas)
# =========================
MONGO_URI = os.environ.get("MONGO_URI")

client = None
collection = None


def create_mongo_client():
    if not MONGO_URI:
        print("⚠️ MONGO_URI environment variable not found")
        return None

    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=20000,
            maxPoolSize=50,
            minPoolSize=5,
            maxIdleTimeMS=30000,
            retryWrites=True,
            w='majority',

            # ✅ FINAL TLS CONFIG (conflict removed)
            tls=True,
            tlsCAFile=certifi.where(),
            tlsDisableOCSPEndpointCheck=True
        )

        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB connected successfully")
        return client

    except ServerSelectionTimeoutError as e:
        print("❌ MongoDB server selection timeout:", e)
        return None
    except ConfigurationError as e:
        print("❌ MongoDB configuration error:", e)
        return None
    except Exception as e:
        print("❌ MongoDB connection error:", e)
        return None


# Initialize connection
client = create_mongo_client()

if client is not None:
    try:
        db = client["iot_db"]
        collection = db["projects"]
    except Exception as e:
        print("❌ Database selection error:", e)
        client = None
        collection = None


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
    return {
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


# =========================
# Routes
# =========================
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/test', methods=['GET'])
def test():
    db_status = "Connected" if collection is not None else "Not Connected"
    return jsonify({
        'message': 'Backend is working',
        'db_status': db_status
    })


@app.route('/api/generate', methods=['POST'])
def generate_project():
    data = request.get_json() or {}
    topic = data.get('topic', '').strip()
    difficulty = data.get('difficulty', 'Beginner')
    category = data.get('category', 'Home Automation')

    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    try:
        if collection is not None:
            project = collection.find_one({
                "category": category,
                "difficulty": difficulty
            })
            if project:
                if '_id' in project:
                    project["_id"] = str(project["_id"])
                return jsonify({'success': True, 'project': project})

        # Fallback
        project_data = _build_project(topic, difficulty, category)
        return jsonify({'success': True, 'project': project_data})

    except Exception as e:
        print(f"Generate error: {e}")
        project_data = _build_project(topic, difficulty, category)
        return jsonify({'success': True, 'project': project_data})


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

        return jsonify({
            'success': True,
            'ideas': [
                {"title": "Smart Plant Watering", "overview": "Auto watering system"},
                {"title": "Smart Light Control", "overview": "Voice control"},
                {"title": "Smart Door Lock", "overview": "Secure entry"},
                {"title": "Smart Temperature Monitor", "overview": "Remote sensing"}
            ]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/save', methods=['POST'])
def save_project():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        if collection is not None:
            data.pop('_id', None)
            result = collection.insert_one(data)
            return jsonify({'success': True, 'id': str(result.inserted_id)})

        return jsonify({'error': 'Database not connected'}), 503

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =========================
# Run server
# =========================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)