import io
import os
import unittest

from app import app
from matching import (
    compute_match_score,
    generate_suggestions,
    get_matching_and_missing_skills,
)


class BackendTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_compute_match_score_returns_scaled_value(self):
        score = compute_match_score("Python developer with Flask and SQL", "Python developer with Flask")
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 100.0)

    def test_skill_matching_is_case_insensitive(self):
        matching, missing = get_matching_and_missing_skills(
            ["Python", "Flask", "SQL"],
            ["python", "pandas", "flask"],
        )
        self.assertEqual(matching, ["Python", "Flask"])
        self.assertEqual(missing, ["Pandas"])

    def test_suggestions_are_generated(self):
        suggestions = generate_suggestions(["Docker", "AWS"], 40)
        self.assertGreaterEqual(len(suggestions), 3)
        self.assertLessEqual(len(suggestions), 5)
        self.assertTrue(any("tailor" in item.lower() for item in suggestions))

    def test_analyze_endpoint_rejects_missing_job_description(self):
        response = self.client.post(
            "/api/analyze",
            data={"job_description": "   "},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_analyze_endpoint_returns_analysis(self):
        resume_data = io.BytesIO(b"Python developer experienced in Flask and SQL")
        response = self.client.post(
            "/api/analyze",
            data={
                "resume_file": (resume_data, "resume.txt"),
                "job_description": "Python developer with Flask and SQL",
            },
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("match_score", payload)
        self.assertIn("matching_skills", payload)
        self.assertIn("missing_skills", payload)
        self.assertIn("suggestions", payload)


if __name__ == "__main__":
    unittest.main()
