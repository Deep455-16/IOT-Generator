from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import json
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# =========================
# Load projects.json
# =========================
PROJECTS_FILE = "projects.json"
try:
    with open(PROJECTS_FILE, "r") as f:
        projects = json.load(f)
    print(f"✅ Loaded {len(projects)} projects from {PROJECTS_FILE}")
except Exception as e:
    print(f"❌ Failed to load {PROJECTS_FILE}: {e}")
    projects = []

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
    """Fallback generator if JSON data not available"""
    rng = _seeded_random(topic, difficulty, category)
    components = [
        {"name": "ESP32", "quantity": 1, "purpose": "Controller", "approximate_cost": "$8"},
        {"name": "Sensor", "quantity": rng.randint(1,3), "purpose": "Input", "approximate_cost": "$5"},
        {"name": "Buzzer", "quantity": 1, "purpose": "Output", "approximate_cost": "$2"},
        {"name": "LED", "quantity": rng.randint(2,5), "purpose": "Indicator", "approximate_cost": "$1 each"}
    ]
    rng.shuffle(components)
    return {
        "title": _format_title(topic, category),
        "tagline": f"A {difficulty} {category} project.",
        "overview": f"This project helps build a {topic.lower()} system.",
        "difficulty": difficulty,
        "category": category,
        "estimated_time": f"{3 + rng.randint(0,2)}-{5 + rng.randint(0,3)} hours",
        "estimated_cost": f"${30 + rng.randint(0,20)}–${60 + rng.randint(0,30)}",
        "components": components[:3],  # Take 3 random components
        "steps": ["Step 1: Setup hardware", "Step 2: Connect components", "Step 3: Run code"],
        "code": {
            "language": "Python",
            "main_code": "# Sample Code\nprint('Hello IoT')",
            "explanation": "This is a basic template for your IoT project"
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
    return jsonify({'message': 'Backend is working'})

@app.route('/api/generate', methods=['POST'])
def generate_project():
    data = request.get_json() or {}
    topic = data.get('topic', '').strip()
    difficulty = data.get('difficulty', 'Beginner').capitalize()
    category = data.get('category', 'Home Automation')

    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    try:
        # Filter JSON projects (case-insensitive)
        filtered = [
            p for p in projects
            if p.get("category", "").lower() == category.lower()
            and p.get("difficulty", "").capitalize() == difficulty
        ]
        if filtered:
            project = filtered[0]  # Return first match
            return jsonify({'success': True, 'project': project})

        # Fallback if JSON doesn't contain a match
        project_data = _build_project(topic, difficulty, category)
        return jsonify({'success': True, 'project': project_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quick-ideas', methods=['POST'])
def quick_ideas():
    data = request.get_json() or {}
    category = data.get('category', 'Home Automation')
    difficulty = data.get('difficulty', 'Beginner').capitalize()

    try:
        filtered = [
            {"title": p.get("title"), "overview": p.get("overview")}
            for p in projects
            if p.get("category", "").lower() == category.lower()
            and p.get("difficulty", "").capitalize() == difficulty
        ]
        if filtered:
            return jsonify({'success': True, 'ideas': filtered[:4]})

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
        # Append to JSON file locally
        projects.append(data)
        with open(PROJECTS_FILE, "w") as f:
            json.dump(projects, f, indent=2)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =========================
# Run server
# =========================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)