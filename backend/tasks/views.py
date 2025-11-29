from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TaskSerializer
from .scoring import calculate_score, detect_circular_dependencies
from datetime import datetime

@api_view(["POST"])
def analyze_tasks(request):
    tasks = request.data

    # Convert string dates → date objects
    for t in tasks:
        t["due_date"] = datetime.strptime(t["due_date"], "%Y-%m-%d").date()

    if detect_circular_dependencies(tasks):
        return Response({"error": "Circular dependencies detected."}, status=400)

    # Compute scores
    tasks_dict = {t["title"]: t for t in tasks}
    for t in tasks:
        score, explanation = calculate_score(t, tasks_dict)
        t["score"] = score
        t["explanation"] = explanation

    tasks_sorted = sorted(tasks, key=lambda x: x["score"], reverse=True)
    return Response(tasks_sorted)


@api_view(["GET"])
def suggest_tasks(request):
    # For demo: expects tasks passed as query param "tasks_json"
    import json

    tasks = json.loads(request.GET.get("tasks", "[]"))

    # Convert dates
    for t in tasks:
        t["due_date"] = datetime.strptime(t["due_date"], "%Y-%m-%d").date()

    scored = []
    for t in tasks:
        s, e = calculate_score(t, {})
        t["score"] = s
        t["explanation"] = e
        scored.append(t)

    return Response(sorted(scored, key=lambda x: x["score"], reverse=True)[:3])
