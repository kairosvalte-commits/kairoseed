"""
Tests for the memory system.
"""

import unittest
from memory.memory import Memory
from models.decision import Decision
from models.hypothesis import Hypothesis


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.memory = Memory(storage_path="memory/store_test.json")
        self.memory.clear()

    def tearDown(self):
        try:
            import os
            os.remove("memory/store_test.json")
        except OSError:
            pass

    def test_weight_update_normalizes(self):
        initial = self.memory.get_weights()
        self.memory.update_weights(predicted_score=0.5, actual_outcome=0.9)
        weights = self.memory.get_weights()
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=6)
        self.assertNotEqual(weights, initial)

    def test_store_decision(self):
        hypothesis = Hypothesis.create("Test hypothesis")
        decision = Decision(
            input_state="test",
            selected_hypothesis=hypothesis,
            decision_text="execute hypothesis",
            confidence_score=0.8
        )
        self.memory.store_decision(decision)
        self.assertEqual(len(self.memory.decision_history), 1)

    def test_get_recent_history(self):
        self.memory.decision_history = []
        for _ in range(3):
            hypothesis = Hypothesis.create("Test hypothesis")
            decision = Decision(
                input_state="test",
                selected_hypothesis=hypothesis,
                decision_text="execute hypothesis",
                confidence_score=0.8
            )
            self.memory.store_decision(decision)
        recent = self.memory.get_recent_history(limit=2)
        self.assertEqual(len(recent), 2)


if __name__ == '__main__':
    unittest.main()
