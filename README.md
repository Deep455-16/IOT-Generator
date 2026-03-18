# ⚡ IoT Forge — Project Generator

A fully integrated frontend-backend IoT project generator with:
- **Python Flask** backend with a rich project database
- **HTML/CSS/JS** frontend with dark tech aesthetic
- Step-by-step guides with real source code for every project
- Filtering by category, difficulty, and search
- Interactive modal with component lists, wiring diagrams, and pro tips

---
# Website Link- https://iot-generator.onrender.com 

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install flask flask-cors
```

### 2. Run the server
```bash
cd IOT-Generator
python app.py
```

### 3. Open in browser
```
http://localhost:5000
```

---

## 📁 Project Structure

```
iot-generator/
├── app.py              ← Flask backend (API + server)
├── requirements.txt    ← Python dependencies
└── templates/
    └── index.html      ← Full frontend (HTML + CSS + JS)
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve the frontend |
| `/api/projects` | GET | List all projects (filterable) |
| `/api/project/<id>` | GET | Full project details |
| `/api/categories` | GET | Categories & difficulty levels |
| `/api/stats` | GET | Summary statistics |

### Query Parameters (GET /api/projects)
- `category` — Filter by category (e.g. `Smart Home`, `Agriculture`)
- `difficulty` — Filter by difficulty (`Beginner`, `Intermediate`, `Advanced`)
- `search` — Full-text search across title, description, technologies

---

## 🧩 Included Projects

| ID | Title | Category | Difficulty |
|----|-------|----------|------------|
| sh001 | Smart Home Automation System | Smart Home | Intermediate |
| ag001 | Smart Irrigation System | Agriculture | Beginner |
| hl001 | Wearable Health Monitor | Healthcare | Advanced |
| ev001 | Air Quality Monitoring Station | Environment | Intermediate |
| sc001 | Smart Security Camera System | Security | Advanced |
| en001 | Solar Energy Monitor | Energy | Intermediate |

---

## ➕ Adding More Projects

In `app.py`, add new entries to the `IOT_PROJECTS` dict following the schema:

```python
{
    "id": "xx001",
    "title": "Project Title",
    "category": "Category Name",
    "difficulty": "Beginner|Intermediate|Advanced",
    "duration": "X weeks",
    "cost": "$XX–$XX",
    "description": "...",
    "components": [
        {"name": "Component", "qty": 1, "purpose": "..."}
    ],
    "technologies": ["Tech1", "Tech2"],
    "steps": [
        {
            "step": 1,
            "title": "Step Name",
            "duration": "X hours",
            "details": "What to do...",
            "code": "// Arduino code..."
        }
    ],
    "circuit_description": "Pin connections...",
    "tips": ["Tip 1", "Tip 2"]
}
```
