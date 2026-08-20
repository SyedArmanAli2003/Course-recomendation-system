import unittest

from validators import normalize_list, validate_level, validate_top_n


class ValidatorTests(unittest.TestCase):
    def test_duplicate_skills_are_removed_case_insensitively(self):
        result = normalize_list("Python, python, SQL, PYTHON")
        self.assertEqual(result, ["python", "sql"])

    def test_valid_level_is_normalized(self):
        self.assertEqual(validate_level(" BEGINNER "), "Beginner")

    def test_invalid_level_raises_error(self):
        with self.assertRaises(ValueError):
            validate_level("SuperExpert")

    def test_invalid_top_n_raises_error(self):
        with self.assertRaises(ValueError):
            validate_top_n(0)

    def test_valid_top_n(self):
        self.assertEqual(validate_top_n("5"), 5)


if __name__ == "__main__":
    unittest.main()
