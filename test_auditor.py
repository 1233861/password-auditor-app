"""
Unit tests for auditor.py's strength-analysis logic.
Run with: python -m pytest test_auditor.py -v
(or just: python test_auditor.py)
"""

import unittest
from auditor import analyze_strength


class TestStrengthAnalysis(unittest.TestCase):

    def test_common_password_is_very_weak(self):
        result = analyze_strength("password")
        self.assertEqual(result.score, 0)
        self.assertEqual(result.label, "Very Weak")

    def test_short_password_flagged(self):
        result = analyze_strength("abc")
        self.assertIn("Use at least 12 characters.", result.feedback)

    def test_strong_password_scores_high(self):
        result = analyze_strength("Tr0ub4dor&3xyz!")
        self.assertGreaterEqual(result.score, 3)
        self.assertTrue(result.has_upper)
        self.assertTrue(result.has_lower)
        self.assertTrue(result.has_digit)
        self.assertTrue(result.has_symbol)

    def test_character_detection(self):
        result = analyze_strength("abc123")
        self.assertTrue(result.has_lower)
        self.assertTrue(result.has_digit)
        self.assertFalse(result.has_upper)
        self.assertFalse(result.has_symbol)

    def test_entropy_increases_with_length(self):
        short = analyze_strength("Ab1!")
        longer = analyze_strength("Ab1!Ab1!Ab1!")
        self.assertGreater(longer.entropy_bits, short.entropy_bits)


if __name__ == "__main__":
    unittest.main()
