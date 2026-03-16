from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import anthropic
import json
import os
import anthropic

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

client = anthropic.Anthropic()

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate_project():
    data = request.get_json()
    topic = data.get('topic', '')
    difficulty = data.get('difficulty', 'Beginner')
    category = data.get('category', 'Home Automation')

    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    prompt = f"""You are an expert IoT engineer and educator. Generate a comprehensive IoT project guide for the following:

Project Topic: {topic}
Difficulty Level: {difficulty}
Category: {category}

Respond ONLY with a valid JSON object (no markdown, no backticks) with this exact structure:
{{
  "title": "Project Title",
  "tagline": "One-line catchy description",
  "overview": "2-3 sentence project overview",
  "difficulty": "{difficulty}",
  "category": "{category}",
  "estimated_time": "e.g. 4-6 hours",
  "estimated_cost": "e.g. $25–$40",
  "components": [
    {{"name": "Component Name", "quantity": 1, "purpose": "What it does", "approximate_cost": "$X"}}
  ],
  "tools_required": ["Tool 1", "Tool 2"],
  "prerequisites": ["Skill/knowledge 1", "Skill/knowledge 2"],
  "architecture": {{
    "description": "Brief architecture overview",
    "layers": [
      {{"name": "Layer Name", "description": "What this layer does", "components": ["component1"]}}
    ]
  }},
  "circuit_description": "Detailed text description of how to wire the circuit",
  "steps": [
    {{
      "step_number": 1,
      "title": "Step Title",
      "description": "Detailed step description",
      "duration": "e.g. 30 minutes",
      "code_snippet": "// Optional code snippet or empty string",
      "tips": ["Tip 1", "Tip 2"]
    }}
  ],
  "code": {{
    "language": "Python/C++/MicroPython etc.",
    "main_code": "// Full working code here",
    "explanation": "Code explanation"
  }},
  "testing": {{
    "steps": ["Test step 1", "Test step 2"],
    "expected_output": "What you should see/observe"
  }},
  "troubleshooting": [
    {{"problem": "Common problem", "solution": "How to fix it"}}
  ],
  "extensions": ["Extension idea 1", "Extension idea 2", "Extension idea 3"],
  "learning_outcomes": ["What you'll learn 1", "What you'll learn 2"]
}}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        raw = message.content[0].text.strip()
        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()
        
        project_data = json.loads(raw)
        return jsonify({'success': True, 'project': project_data})
    
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Failed to parse project data: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/quick-ideas', methods=['POST'])
def quick_ideas():
    data = request.get_json()
    category = data.get('category', 'Home Automation')
    difficulty = data.get('difficulty', 'Beginner')

    prompt = f"""Generate 6 creative IoT project ideas for category: {category}, difficulty: {difficulty}.
Respond ONLY with a JSON array (no markdown):
[
  {{"title": "Project Name", "description": "One sentence description", "components": ["Arduino", "Sensor"], "wow_factor": "What makes it cool"}}
]"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()
        ideas = json.loads(raw)
        return jsonify({'success': True, 'ideas': ideas})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
