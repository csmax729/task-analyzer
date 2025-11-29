from django.test import TestCase
from datetime import date, timedelta
from .scoring import calculate_score, detect_circular_dependencies

class ScoringTests(TestCase):

    def test_score_increases_with_importance(self):
        t1 = {"title": "A", "due_date": date.today(), "estimated_hours": 5, "importance": 3, "dependencies": []}
        t2 = {"title": "B", "due_date": date.today(), "estimated_hours": 5, "importance": 8, "dependencies": []}

        s1, _ = calculate_score(t1, {})
        s2, _ = calculate_score(t2, {})

        self.assertGreater(s2, s1)

    def test_past_due_has_high_urgency(self):
        past = {"title": "Late", "due_date": date.today() - timedelta(days=3),
                "estimated_hours": 4, "importance": 5, "dependencies": []}
        score, _ = calculate_score(past, {})

        self.assertGreater(score, 5)

    def test_circular_dependencies(self):
        tasks = [
            {"title": "A", "dependencies": ["B"]},
            {"title": "B", "dependencies": ["A"]},
        ]
        self.assertTrue(detect_circular_dependencies(tasks))
