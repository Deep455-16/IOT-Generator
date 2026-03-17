from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import anthropic

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Ensure the Anthropic API key is set in the environment.
# Set it like:
#   setx ANTHROPIC_API_KEY "your_api_key"  (Windows)
# or
#   export ANTHROPIC_API_KEY="your_api_key"  (macOS/Linux)
API_KEY = os.environ.get('ANTHROPIC_API_KEY')
if not API_KEY:
    raise RuntimeError(
        'Missing ANTHROPIC_API_KEY in environment. Set this env var before running the server.'
    )

client = anthropic.Anthropic(api_key=API_KEY)

def _extract_text_from_message(message):
    """Extract a single plain-text string from an Anthropic Message object."""
    if not message:
        return ""
    # The API returns a list of content blocks; each block has type and text.
    # We'll join all `text` fields in text blocks.
    content = getattr(message, 'content', None) or message.get('content') if isinstance(message, dict) else None
    if not content:
        return ""
    if isinstance(content, str):
        return content
    parts = []
    for block in content:
        if isinstance(block, dict):
            if block.get('type') == 'text' and 'text' in block:
                parts.append(block.get('text', ''))
        else:
            # Some SDK versions may return types with .type/.text attributes
            if getattr(block, 'type', None) == 'text':
                parts.append(getattr(block, 'text', '') or '')
    return "".join(parts).strip()


def _clean_json_text(raw):
    """Strip markdown/code fences and whitespace to get a clean JSON string."""
    if not isinstance(raw, str):
        return raw
    raw = raw.strip()

    # Remove leading/trailing code fences (``` or ```json)
    if raw.startswith('```'):
        raw = raw.split('```', 2)[-1]
    if raw.lstrip().startswith('json'):
        raw = raw.lstrip()[4:]
    return raw.strip()


def _call_anthropic(prompt: str, model: str = 'claude-3.5-haiku-latest', max_tokens: int = 2500):
    """Call the Anthropic Messages API and return the assistant text response."""
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # The response is a Message object; extract its generated text.
    return _extract_text_from_message(response)


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
        raw = _call_anthropic(prompt)
        cleaned = _clean_json_text(raw)
        project_data = json.loads(cleaned)
        return jsonify({'success': True, 'project': project_data})

    except json.JSONDecodeError as e:
        return jsonify({'error': f'Failed to parse project data: {str(e)}', 'response': raw}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/quick-ideas', methods=['POST'])
def quick_ideas():
    data = request.get_json() or {}
    category = data.get('category', 'Home Automation')
    difficulty = data.get('difficulty', 'Beginner')

    prompt = f"""You are an AI assistant that generates short IoT project idea summaries.

Generate 4 unique IoT project ideas for the following category and difficulty:

Category: {category}
Difficulty: {difficulty}

Return a JSON object with the following structure:
{{
  "ideas": [
    {{
      "title": "Project title",
      "description": "1-2 sentence description",
      "components": ["component 1", "component 2"],
      "wow_factor": "Why this idea is exciting"
    }}
  ]
}}

Respond only with valid JSON (no markdown, no backticks)."""

    try:
        raw = _call_anthropic(prompt, max_tokens=1200)
        cleaned = _clean_json_text(raw)
        ideas_data = json.loads(cleaned)
        return jsonify({'success': True, 'ideas': ideas_data.get('ideas', [])})
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Failed to parse ideas data: {str(e)}', 'response': raw}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
