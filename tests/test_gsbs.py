"""
Tests for GSBS (Generalized Scoring and Selection System).
"""

import unittest
from core.gsbs import GSBS, HypothesisScore
from models.hypothesis import Hypothesis


class TestGSBS(unittest.TestCase):
    """Test cases for GSBS scoring system."""

    def setUp(self):
        """Set up test fixtures."""
        self.scorer = GSBS()
        self.hypotheses = [
            Hypothesis.create("Direct approach to problem"),
            Hypothesis.create("Conservative strategy"),
            Hypothesis.create("Aggressive solution")
        ]

    def test_hypothesis_scoring(self):
        """Test that hypotheses get scores."""
        scores = self.scorer.score_hypotheses(self.hypotheses)

        self.assertEqual(len(scores), len(self.hypotheses))
        for score in scores:
            self.assertIsInstance(score, HypothesisScore)
            self.assertGreaterEqual(score.score, -1.0)
            self.assertLessEqual(score.score, 1.0)

    def test_best_selection(self):
        """Test selection of best hypothesis."""
        scores = self.scorer.score_hypotheses(self.hypotheses)
        best_hyp, best_score = self.scorer.select_best(self.hypotheses, scores)

        self.assertIsNotNone(best_hyp)
        self.assertIsNotNone(best_score)
        self.assertEqual(best_hyp.id, best_score.hypothesis_id)

        # Best score should be the highest
        all_scores = [s.score for s in scores]
        self.assertEqual(best_score.score, max(all_scores))

    def test_weight_updates(self):
        """Test weight adjustment functionality."""
        original_weights = self.scorer.weights.copy()

        # Simulate positive feedback
        feedback = {'success': 0.1, 'cost': -0.05}
        self.scorer.update_weights(feedback)

        # Weights should have changed
        self.assertNotEqual(self.scorer.weights, original_weights)

    def test_score_calculation(self):
        """Test score calculation formula."""
        # Create a score with known values
        score = HypothesisScore(
            hypothesis_id="test",
            success=0.8,
            stability=0.6,
            cost=0.3,
            risk=0.2,
            weights={'success': 0.4, 'stability': 0.3, 'cost': 0.2, 'risk': 0.1}
        )

        expected = (0.4 * 0.8) + (0.3 * 0.6) - (0.2 * 0.3) - (0.1 * 0.2)
        self.assertAlmostEqual(score.score, expected, places=5)

    def test_empty_hypotheses(self):
        """Test behavior with empty hypothesis list."""
        best_hyp, best_score = self.scorer.select_best([])
        self.assertIsNone(best_hyp)
        self.assertIsNone(best_score)


if __name__ == '__main__':
    unittest.main()