from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import random

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)


def _seeded_random(topic: str, difficulty: str, category: str):
    """Create a deterministic random generator based on the request."""
    seed = f"{topic}|{difficulty}|{category}"
    return random.Random(seed)


def _format_title(topic: str, category: str):
    if topic.lower().startswith('smart'):
        return topic.title()
    return f"Smart {topic.title()} System"


def _get_category_components(category: str):
    """Return a set of default components for a given category."""
    common = [
        {"name": "ESP32 / Arduino", "quantity": 1, "purpose": "Main microcontroller", "approximate_cost": "$8"},
        {"name": "Breadboard", "quantity": 1, "purpose": "Prototyping and wiring", "approximate_cost": "$5"},
        {"name": "Jumper wires", "quantity": 20, "purpose": "Connect components", "approximate_cost": "$3"},
        {"name": "USB power supply", "quantity": 1, "purpose": "Power the system", "approximate_cost": "$7"},
    ]

    category_map = {
        "Home Automation": [
            {"name": "Relay module", "quantity": 1, "purpose": "Switch AC loads", "approximate_cost": "$6"},
            {"name": "Temperature sensor (DHT22)", "quantity": 1, "purpose": "Measure temperature and humidity", "approximate_cost": "$8"},
            {"name": "Light sensor", "quantity": 1, "purpose": "Detect ambient light", "approximate_cost": "$4"},
        ],
        "Security": [
            {"name": "PIR motion sensor", "quantity": 1, "purpose": "Detect movement", "approximate_cost": "$5"},
            {"name": "Buzzer", "quantity": 1, "purpose": "Alarm output", "approximate_cost": "$2"},
            {"name": "Camera module", "quantity": 1, "purpose": "Capture images/video", "approximate_cost": "$15"},
        ],
        "Environment": [
            {"name": "Air quality sensor", "quantity": 1, "purpose": "Measure VOCs and PM2.5", "approximate_cost": "$12"},
            {"name": "Soil moisture sensor", "quantity": 1, "purpose": "Monitor soil humidity", "approximate_cost": "$6"},
            {"name": "Water pump", "quantity": 1, "purpose": "Automated watering", "approximate_cost": "$10"},
        ],
        "Healthcare": [
            {"name": "Pulse sensor", "quantity": 1, "purpose": "Measure heart rate", "approximate_cost": "$8"},
            {"name": "OLED display", "quantity": 1, "purpose": "Show readings", "approximate_cost": "$10"},
            {"name": "Pressure sensor", "quantity": 1, "purpose": "Capture force/pressure readings", "approximate_cost": "$7"},
        ],
        "Energy": [
            {"name": "Current sensor", "quantity": 1, "purpose": "Measure electrical current", "approximate_cost": "$7"},
            {"name": "Voltage divider", "quantity": 1, "purpose": "Measure voltage safely", "approximate_cost": "$3"},
            {"name": "LCD display", "quantity": 1, "purpose": "Show power metrics", "approximate_cost": "$10"},
        ],
        "Agriculture": [
            {"name": "Soil moisture sensor", "quantity": 1, "purpose": "Track soil hydration", "approximate_cost": "$6"},
            {"name": "Water pump", "quantity": 1, "purpose": "Automate irrigation", "approximate_cost": "$10"},
            {"name": "Ambient light sensor", "quantity": 1, "purpose": "Monitor sunlight", "approximate_cost": "$4"},
        ],
        "Education": [
            {"name": "LCD display", "quantity": 1, "purpose": "Display status and data", "approximate_cost": "$10"},
            {"name": "Button set", "quantity": 3, "purpose": "User input", "approximate_cost": "$3"},
            {"name": "RGB LED", "quantity": 3, "purpose": "Visual feedback", "approximate_cost": "$2"},
        ],
    }
    return common + category_map.get(category, [])


def _estimate_cost_and_time(difficulty: str):
    mapping = {
        "Beginner": ("2-4 hours", "$20–$40"),
        "Intermediate": ("4-6 hours", "$40–$80"),
        "Advanced": ("6-10 hours", "$80–$150"),
    }
    return mapping.get(difficulty, ("3-5 hours", "$30–$60"))


def _generate_steps(rng: random.Random, difficulty: str):
    base_steps = [
        {
            "title": "Gather Components",
            "description": "Collect and verify all hardware parts needed for the project.",
            "duration": "30 minutes",
            "code_snippet": "",
            "tips": [
                "Double-check pin labels before wiring.",
                "Use a breadboard or prototype board for clean wiring."
            ],
        },
        {
            "title": "Build the Circuit",
            "description": "Wire the sensors and actuators to the microcontroller following the schematic.",
            "duration": "45 minutes",
            "code_snippet": "",
            "tips": [
                "Keep power and signal wiring separate to reduce noise.",
                "Use consistent color coding for wires."
            ],
        },
        {
            "title": "Write the Firmware",
            "description": "Write and upload the code that reads sensors and controls outputs.",
            "duration": "60 minutes",
            "code_snippet": "",
            "tips": [
                "Start with a minimal sketch that prints sensor values.",
                "Comment your code so it's easy to revisit."
            ],
        },
        {
            "title": "Test the System",
            "description": "Verify each component works and the system behaves as expected.",
            "duration": "30 minutes",
            "code_snippet": "",
            "tips": [
                "Test one sensor at a time before combining them.",
                "Use the serial monitor to debug sensor readings."
            ],
        },
        {
            "title": "Polish and Expand",
            "description": "Add features like logging, remote access, or improved UI.",
            "duration": "45 minutes",
            "code_snippet": "",
            "tips": [
                "Keep your code modular so new features are easy to add.",
                "Document your changes for future reference."
            ],
        },
    ]

    if difficulty == "Beginner":
        return [{**s, "step_number": i + 1} for i, s in enumerate(base_steps[:4])]
    if difficulty == "Advanced":
        extra = {
            "title": "Add Remote Monitoring",
            "description": "Integrate network connectivity and remote dashboards.",
            "duration": "60 minutes",
            "code_snippet": "",
            "tips": [
                "Use MQTT or HTTP APIs for reliable data transport.",
                "Keep credentials out of source control (use environment variables)."
            ],
        }
        base_steps.append(extra)

    return [{**s, "step_number": i + 1} for i, s in enumerate(base_steps)]


def _generate_code_snippet(category: str, topic: str):
    # Simple template that the frontend can display.
    template = (
        "# {topic} project code template\n"
        "# Replace the sensor pins and logic with your specific hardware\n\n"
        "def setup():\n"
        "    print('Initializing {topic}')\n"
        "\n"
        "def loop():\n"
        "    # Read sensor values\n"
        "    # TODO: Add your read + control logic here\n"
        "    pass\n\n"
        "if __name__ == '__main__':\n"
        "    setup()\n"
        "    while True:\n"
        "        loop()\n"
    )
    return template.format(topic=topic)


def _build_project(topic: str, difficulty: str, category: str):
    rng = _seeded_random(topic, difficulty, category)
    title = _format_title(topic, category)
    estimated_time, estimated_cost = _estimate_cost_and_time(difficulty)

    components = _get_category_components(category)
    rng.shuffle(components)

    project = {
        "title": title,
        "tagline": f"A {difficulty.lower()} {category.lower()} project that teaches you how to build a {topic.lower()} system.",
        "overview": f"This project walks you through building a {topic.lower()} system using readily available IoT hardware. You'll learn the hardware setup, software, and testing process to get a working prototype.",
        "difficulty": difficulty,
        "category": category,
        "estimated_time": estimated_time,
        "estimated_cost": estimated_cost,
        "components": components[:6],
        "tools_required": [
            "Screwdriver set",
            "Wire cutters/strippers",
            "Computer with USB port",
            "Multimeter (optional)"
        ],
        "prerequisites": [
            "Basic programming knowledge",
            "Familiarity with breadboards and wiring",
        ],
        "architecture": {
            "description": "A simple IoT architecture with sensors feeding data to a microcontroller, optionally sending updates to a dashboard.",
            "layers": [
                {
                    "name": "Sensing",
                    "description": "Collects data from the physical world.",
                    "components": [c["name"] for c in components[:2]]
                },
                {
                    "name": "Control",
                    "description": "Processes inputs and drives outputs.",
                    "components": ["ESP32 / Arduino"]
                },
                {
                    "name": "Interface",
                    "description": "Optional user interface or remote dashboard.",
                    "components": ["OLED display", "Wi‑Fi module"]
                },
            ]
        },
        "circuit_description": "Wire the sensors and actuators to the microcontroller according to each module's pinout, with power and ground rails connected to the board.",
        "steps": _generate_steps(rng, difficulty),
        "code": {
            "language": "Python",
            "main_code": _generate_code_snippet(category, topic),
            "explanation": "This template provides a structure for reading sensors and controlling outputs. Replace the placeholders with your specific hardware logic."
        },
        "testing": {
            "steps": [
                "Power the system and verify the microcontroller boots.",
                "Confirm sensor readings are within expected ranges.",
                "Trigger actuators and confirm they respond correctly."
            ],
            "expected_output": "The system should read sensor values and respond as described in the project steps."
        },
        "troubleshooting": [
            {"problem": "The board won't power on", "solution": "Check the power supply and USB connection, and ensure the voltage is correct."},
            {"problem": "Sensors return unexpected values", "solution": "Verify your wiring, sensor orientation, and that the correct pins are used in code."},
        ],
        "extensions": [
            "Add a mobile dashboard to monitor data in real time.",
            "Implement remote notifications (email/SMS) when thresholds are crossed.",
            "Add data logging to an SD card or cloud service."
        ],
        "learning_outcomes": [
            "Understand how to wire sensors and actuators to a microcontroller.",
            "Write firmware to read sensors and control actuators.",
            "Test and troubleshoot a basic IoT system."
        ]
    }

    return project


def _generate_ideas(category: str, difficulty: str):
    base_ideas = [
        "Smart Plant Watering System",
        "Home Energy Tracker",
        "Air Quality Monitor",
        "DIY Security Camera",
        "Wearable Health Monitor",
        "Weather Station"
    ]

    rng = _seeded_random(category, difficulty, "ideas")
    rng.shuffle(base_ideas)

    ideas = []
    for title in base_ideas[:4]:
        ideas.append({
            "title": title,
            "description": f"A {difficulty.lower()} project that uses sensors and a microcontroller to build a {title.lower()}.",
            "components": ["ESP32 / Arduino", "Sensors", "Power supply"],
            "wow_factor": "Shows real-world sensing and control in a compact package."
        })
    return ideas


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
        ideas = _generate_ideas(category, difficulty)
        return jsonify({'success': True, 'ideas': ideas})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
