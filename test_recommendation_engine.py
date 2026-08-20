import unittest

from models import Course, UserProfile
from recommendation_engine import RecommendationEngine


class RecommendationEngineTests(unittest.TestCase):
    def setUp(self):
        self.perfect_course = Course(
            course_id="T001",
            title="Machine Learning Fundamentals",
            category="AI",
            level="Beginner",
            interests=["Artificial Intelligence", "Machine Learning"],
            prerequisites=["Python"],
            skills_taught=["Machine Learning"],
            career_goals=["ML Engineer"],
            description="Test course",
        )

        self.advanced_course = Course(
            course_id="T002",
            title="Advanced Deep Learning",
            category="AI",
            level="Advanced",
            interests=["Artificial Intelligence"],
            prerequisites=["Python", "Machine Learning", "Linear Algebra"],
            skills_taught=["Deep Learning"],
            career_goals=["ML Engineer"],
            description="Advanced test course",
        )

        self.no_prereq_course = Course(
            course_id="T003",
            title="Git Essentials",
            category="Software",
            level="Beginner",
            interests=["Software Engineering"],
            prerequisites=[],
            skills_taught=["Git"],
            career_goals=["Backend Developer"],
            description="No prerequisite course",
        )

        self.profile = UserProfile(
            skills=["Python"],
            interests=["Artificial Intelligence", "Machine Learning"],
            level="Beginner",
            goal="ML Engineer",
        )

    def test_exact_match_scores_100(self):
        engine = RecommendationEngine([self.perfect_course])
        result = engine.score_course(self.perfect_course, self.profile)
        self.assertEqual(result.score, 100.0)
        self.assertTrue(result.eligible)

    def test_beginner_user_cannot_take_advanced_course(self):
        engine = RecommendationEngine([self.advanced_course])
        result = engine.score_course(self.advanced_course, self.profile)
        self.assertFalse(result.eligible)

    def test_missing_prerequisites_are_reported(self):
        engine = RecommendationEngine([self.advanced_course])
        result = engine.score_course(self.advanced_course, self.profile)
        self.assertIn("Machine Learning", result.missing_prerequisites)
        self.assertIn("Linear Algebra", result.missing_prerequisites)

    def test_course_with_no_prerequisites_gets_full_prerequisite_points(self):
        profile = UserProfile(
            skills=[],
            interests=["Software Engineering"],
            level="Beginner",
            goal="Backend Developer",
        )
        engine = RecommendationEngine([self.no_prereq_course])
        result = engine.score_course(self.no_prereq_course, profile)
        self.assertTrue(result.eligible)
        self.assertEqual(result.score, 100.0)

    def test_recommend_returns_only_requested_top_n(self):
        second_course = Course(
            course_id="T004",
            title="Intro to AI",
            category="AI",
            level="Beginner",
            interests=["Artificial Intelligence"],
            prerequisites=["Python"],
            skills_taught=["AI"],
            career_goals=["AI Engineer"],
            description="Second test course",
        )
        engine = RecommendationEngine([self.perfect_course, second_course])
        results = engine.recommend(self.profile, top_n=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].course.course_id, "T001")

    def test_case_insensitive_matching(self):
        profile = UserProfile(
            skills=["PYTHON"],
            interests=["MACHINE LEARNING", "ARTIFICIAL INTELLIGENCE"],
            level="beginner",
            goal="ml engineer",
        )
        engine = RecommendationEngine([self.perfect_course])
        result = engine.score_course(self.perfect_course, profile)
        self.assertEqual(result.score, 100.0)


if __name__ == "__main__":
    unittest.main()
