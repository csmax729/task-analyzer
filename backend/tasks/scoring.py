from datetime import date

def detect_circular_dependencies(tasks):
    graph = {t["title"]: t.get("dependencies", []) for t in tasks}
    visited = set()
    stack = set()

    def dfs(node):
        if node in stack:
            return True
        if node in visited:
            return False

        visited.add(node)
        stack.add(node)

        for dep in graph.get(node, []):
            if dfs(dep):
                return True
        stack.remove(node)
        return False

    for t in graph:
        if dfs(t):
            return True

    return False


def calculate_score(task, tasks_dict):
    today = date.today()

    # Urgency (0–10)
    days_left = (task["due_date"] - today).days
    if days_left < 0:
        urgency = 10
    else:
        urgency = max(0, 10 - days_left)

    # Importance (1–10)
    importance = task["importance"]

    # Effort (inverted so lower effort → higher score)
    effort_score = max(1, 10 - task["estimated_hours"])

    # Dependency weight
    dependency_count = len(task.get("dependencies", []))
    dependency_score = min(10, dependency_count * 2)

    # Smart Balanced Score (weighted)
    score = (
        urgency * 0.4 +
        importance * 0.35 +
        effort_score * 0.15 +
        dependency_score * 0.10
    )

    explanation = (
        f"Urgency={urgency}, Imp={importance}, EffortScore={effort_score}, "
        f"Deps={dependency_score}"
    )

    return round(score, 2), explanation
