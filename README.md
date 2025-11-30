Smart Task Analyzer

Overview

Smart Task Analyzer is an intelligent productivity tool that ingests user-defined tasks and ranks them using a custom scoring engine that considers:

--->Urgency (time until deadline)

--->Importance

--->Effort estimates

--->Dependency impact (tasks blocking others)

--->Dynamic strategy modifiers

It exposes a clean REST API built in Django REST Framework and includes a lightweight HTML/JS frontend.


🚀 Features
Backend (Django + DRF)

* Custom scoring algorithm
* Circular dependency detection
* REST API:

  /api/tasks/analyze/ → Full scoring + sorting

  /api/tasks/suggest/ → Top 3 tasks with explanation
    * Extensive validation
    * Unit tests for algorithm correctness

Frontend (HTML + JS)

* JSON-based task input
* Strategy selection (smart / fast / impact / deadline)
* Real-time visualization of ranked tasks

⚙️ Installation & Setup
1. Clone the project
```bash
git clone <your-repo-url>
cd project/backend
```
2. Create a virtual environment
``` bash
python -m venv venv
venv\Scripts\activate        # Windows
```
3.Install dependencies
```bash
pip install -r requirements.txt
```
4. Run migrations
python manage.py migrate

5. Backend runs at:
👉 http://127.0.0.1:8000

Frontend (static) can be opened directly from:
👉 frontend/index.htmlStart the server
python manage.py runserver


🛠 API Documentation
🔍 1. Analyze Tasks
POST /api/tasks/analyze/
Request Body (JSON array)
```bash
[
  {
    "title": "Write report",
    "due_date": "2025-03-20",
    "estimated_hours": 3,
    "importance": 7,
    "dependencies": ["Research topic"]
  }
]
```
Response
```bash

[
  {
    "title": "Write report",
    "due_date": "2025-03-20",
    "score": 7.85,
    "importance": 7,
    "estimated_hours": 3,
    "dependencies": []
  }
]
```
2. Suggested Tasks
GET /api/tasks/suggest/?tasks=[...]

Returns top 3 tasks with reasoning.

Example response:
```bash
[
  {
    "title": "Prepare slides",
    "score": 8.1,
    "reason": "Importance=8, urgency factor applied."
  }
]
```
Scoring Algorithm Internals
The scoring engine evaluates each task based on:

1. Urgency (40%)
```bash
urgency = max(0, 10 - days_remaining)
if overdue: urgency = 10
```
2. Importance (40%)

User-defined (1–10)

3. Quick-wins (effort factor — 15%)
```bash
quick_win = 10 - estimated_hours
```

4. Dependency Impact (25%)
```bash
dependency_count = how many tasks depend on this one
```
Final Score
```bash
score = urgency*0.4 + importance*0.4 + quick_win*0.15 + dependency*0.25
```
Circular Dependency Detection

A depth-first search (DFS) is run across all dependency chains.
If a cycle is detected → API returns error 400.


Frontend Features

The frontend allows:

✔ JSON task entry

Paste a JSON array of tasks into the text area.

✔ Strategy Dropdown

  Smart Balance (default)

  Fastest Wins

  High Impact

  Deadline Driven

These strategies reorder tasks before sending to backend.

✔ Results Display

Formatted JSON printed dynamically.


🧪 Testing

Run backend tests:
```bash
python manage.py test
```
Tests include:

✔ Urgency handling

Past deadlines → highest urgency.

✔ Effort effect

Lower effort → higher score.

✔ Dependency effect

Tasks unblocking others → higher score.

🛡 Error Handling
Invalid JSON → 400
Missing fields → 400
Circular dependencies → 400

```bash
{"error": "Circular dependency detected"}
```
🚀 Deployment Guide
Backend (Django)

Use Gunicorn or Uvicorn

Deploy on AWS / Railway / Render / Heroku

Add CORS if serving frontend separately
```bash
pip install django-cors-headers
```
Frontend

  Host using GitHub Pages / Vercel / Netlify (static)

📄 Sample Task Set
```bash
[
  {
    "title": "Research topic",
    "importance": 8,
    "estimated_hours": 2,
    "due_date": "2025-03-05",
    "dependencies": []
  },
  {
    "title": "Write report",
    "importance": 7,
    "estimated_hours": 4,
    "due_date": "2025-03-10",
    "dependencies": ["Research topic"]
  }
]
```
🏁 Conclusion

This project demonstrates:

  Strong backend architecture

  Solid scoring logic

  Frontend usability

  Clean APIs

  Robust testing

  Clear documentation
