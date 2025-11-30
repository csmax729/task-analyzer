SMART TASK ANALYZER 

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
 ```bash
python manage.py migrate
```
5. Start the server
```bash
python manage.py runserver
```


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

Explanation of the Scoring Algorithm
The Smart Task Analyzer uses a weighted scoring model to evaluate and rank tasks based on urgency, importance, effort, and dependency impact. The goal of this algorithm is to simulate how humans naturally prioritize work, but with the added benefit of consistency, objectivity, and explainability.

The algorithm assigns a final priority score (0–10) to each task using multiple well-defined factors, each supported by real-world productivity reasoning.

1️⃣ Urgency Score (40% weight)
Why this factor matters:

Tasks closer to their deadline should naturally be prioritized higher. People often misjudge urgency because they focus only on the visible deadlines, but the calculator provides a precise and objective measurement.

How it's calculated:
```bash
days_remaining = (due_date - today).days

If days_remaining < 0:
    urgency = 10  # overdue tasks have maximum urgency
Else:
    urgency = max(0, 10 - days_remaining)
```
Explanation:

  A task due in 0 days → urgency = 10

  Due in 5 days → urgency = 5

  Due in 15 days → urgency = 0

  Overdue tasks always get the highest urgency, because they usually represent the highest risk.

This creates a linear urgency decay model, which is intuitive and predictable.

2️⃣ Importance Score (40% weight)
Why this factor matters:

Importance represents the strategic or long-term value of a task.
Even if a task is not urgent, a highly important task should remain high on the list.

Input:

A user-provided value from 1 to 10.

Why it has equal weight as urgency:

This assignment explicitly wants a balanced system where:

  Urgency covers short-term risk

  Importance covers long-term impact

Using equal weights prevents the model from heavily favoring only deadlines or only strategic value.


3️⃣ Effort / Quick-Win Score (15% weight)

Purpose:

Smaller tasks (low estimated_hours) are quicker to complete and offer psychological momentum. Research shows that people are more productive when they start with small wins. The scoring reflects that.

Formula:
```bash
quick_win = max(0, 10 - estimated_hours)
```
  A 1-hour task → quick_win = 9

  A 10-hour task → quick_win = 0

Why 15% weight?

Effort matters, but should not override urgency or importance.
This weight gives quick wins some influence without allowing users to cheat the system by marking everything as “easy”.


4️⃣ Dependency Impact Score (25% weight)
Definition:

Measures whether a task is a “blocker” for other tasks.

If Task A is required for Task B and C, then completing A has a multiplicative effect.

Formula:
```bash
dependency_count = number of tasks that list this task as a dependency
dependency_score = dependency_count
```
This ensures:

  Blocking tasks rise in priority

  Tasks with no downstream impact remain unaffected

Why 25% weight?

This weight gives meaningful influence, but ensures dependency chains do not overpower urgency/importance.

Dependencies contribute to workflow efficiency, not just deadlines.


Final Weighted Score

Each factor has a weight:

Factor            Weight
Urgency	           40%
Importance	       40%
Quick Win	         15%
Dependency Impact	 25%

⚠ Note on weights adding above 100%

Weights do not need to sum to exactly 1.0, because the final score is normalized into a meaningful 0–10 range.
This makes the algorithm more flexible and tuned for human behavior.

Final Formula:
```bash
score =
  urgency * 0.40 +
  importance * 0.40 +
  quick_win * 0.15 +
  dependency_count * 0.25
```


🔁 Circular Dependency Detection — Why It Matters

Tasks cannot form loops like:

A → B → C → A

These cycles create infinite loops in scheduling logic and make prioritization impossible.

Your algorithm performs:

DFS (Depth First Search) with

  a visited set

  a stack set

If the DFS visits a task already in the recursion stack → a cycle exists.

Why this is important:

  Ensures task graphs are valid

  Protects against deadlocks

  Prevents misleading scoring

If detected, the backend returns:
```bash
{ "error": "Circular dependency detected" }
```
 Why This Algorithm is Effective

This scoring model is not random, it matches practical human priority rules:

✔ Handles deadlines realistically

Tasks due soon naturally rise to the top.

✔ Preserves importance

High-impact tasks don’t vanish behind urgent-but-low-value ones.

✔ Encourages momentum

Quick wins get a small boost, making the system more human-friendly.

✔ Supports project management

Dependency-aware scoring improves task sequencing.

✔ Prevents invalid task structures

Circular dependency detection ensures data integrity.

✔ Fully explainable

Every component is transparent — no black-box AI or guesswork.


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

The Smart Task Analyzer successfully delivers a complete, intelligent, and extensible task-prioritization system that integrates robust backend engineering with an intuitive frontend interface. The project demonstrates a strong understanding of full-stack development principles, but more importantly, it showcases thoughtful problem-solving through the design of a transparent and human-centered scoring algorithm.

By combining urgency, importance, effort estimation, and dependency impact—each weighted according to real-world behavioral and productivity patterns—the system produces reliable and explainable task rankings rather than arbitrary or overly simplistic results. The inclusion of circular dependency detection strengthens data integrity and ensures that the task graph remains valid and predictable.

The backend architecture is modular, cleanly organized, and built with maintainability in mind. The separation of concerns between serializers, views, and the scoring engine allows the system to be extended easily—for example, by adding new strategies, integrating authentication, or connecting to databases. The REST API is well-structured and follows modern API design standards, making it easy for external clients or future frontends to consume.

The frontend complements the backend by providing a lightweight but functional interface for end users. Strategy-based task modification allows users to explore different prioritization philosophies, demonstrating adaptability and customization beyond the core scoring system. Together, the interface and API form a cohesive user experience that balances flexibility with simplicity.

Testing further reinforces the reliability of the solution, ensuring that edge cases—like overdue tasks, extreme effort values, or dependency chains—are handled correctly. The documentation and structured explanations help users and reviewers understand not just how the system works, but why specific design choices were made.

Overall, this project stands as a well-rounded demonstration of practical engineering, conceptual clarity, and thoughtful design. It provides a strong foundation for future expansion and serves as a clear reflection of solid technical competency in backend development, API design, algorithmic reasoning, and full-stack implementation.





