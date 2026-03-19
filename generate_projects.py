import json
import random

categories = [
    "Home Automation",
    "Smart Agriculture",
    "Industrial IoT",
    "Healthcare & Wearables",
    "Environmental Monitoring",
    "Smart Energy",
    "Security & Surveillance",
    "Smart Cities",
    "Robotics & Motion",
    "Asset Tracking"
]

difficulties = ["Beginner", "Intermediate", "Advanced"]

base_titles = [
    "Monitoring System", "Control System", "Automation System",
    "Tracking System", "Detection System", "Management System",
    "Alert System", "Optimization System", "Surveillance System",
    "Prediction System"
]

components_pool = [
    "ESP32", "Arduino", "Raspberry Pi", "DHT22", "MQ135",
    "Ultrasonic Sensor", "Relay Module", "LCD Display",
    "OLED Display", "GPS Module", "GSM Module",
    "Camera Module", "Servo Motor", "DC Motor",
    "Battery", "Power Supply", "Breadboard", "Jumper Wires"
]

def generate_project(category, i):
    difficulty = random.choice(difficulties)

    title = f"{category.split()[0]} {random.choice(base_titles)} {i}"

    return {
        "title": title,
        "category": category,
        "difficulty": difficulty,
        "overview": f"This project implements a {title.lower()} using IoT technologies.",
        "components": random.sample(components_pool, 6),
        "code": {
            "language": "Python",
            "main_code": f"print('Running {title}')"
        }
    }

all_projects = []

for category in categories:
    for i in range(1, 51):   # 🔥 50 projects per category
        all_projects.append(generate_project(category, i))

# Save file
with open("projects.json", "w") as f:
    json.dump(all_projects, f, indent=2)

print("✅ 500 Projects Generated!")