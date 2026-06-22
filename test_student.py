import unittest
from student_form import calculate_average, is_duplicate


class TestStudent(unittest.TestCase):

    # Test 1: normal average
    def test_average(self):
        self.assertEqual(calculate_average(90, 80, 70), 80)

    # Test 2: full marks
    def test_full_marks(self):
        self.assertEqual(calculate_average(100, 100, 100), 100)

    # Test 3: zero marks
    def test_zero_marks(self):
        self.assertEqual(calculate_average(0, 0, 0), 0)

    # Test 4: invalid score
    def test_invalid_score(self):
        with self.assertRaises(ValueError):
            calculate_average("A", 90, 80)

    # Test 5: duplicate student (false case)
    def test_duplicate_student(self):
        self.assertFalse(is_duplicate("RandomName"))


if __name__ == '__main__':
    unittest.main()