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
''' bash 
