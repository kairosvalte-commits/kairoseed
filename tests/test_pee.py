"""
Tests for the PEE evolution engine.
"""

import unittest
from core.pee import PEE
from models.hypothesis import Hypothesis
from core.gsbs import GSBS


class TestPEE(unittest.TestCase):
    def setUp(self):
        self.evolver = PEE(mutation_rate=1.0)
        self.scorer = GSBS()
        self.hypotheses = [
            Hypothesis.create("Test hypothesis A"),
            Hypothesis.create("Test hypothesis B")
        ]
        self.scores = self.scorer.score_hypotheses(self.hypotheses)

    def test_mutation_produces_variant(self):
        mutated = self.evolver.mutate(self.hypotheses[0])
        self.assertNotEqual(mutated.id, self.hypotheses[0].id)
        self.assertIn('operation', mutated.metadata)
        self.assertEqual(mutated.metadata['operation'], 'mutation')

    def test_merge_produces_combination(self):
        merged = self.evolver.merge(self.hypotheses[0], self.hypotheses[1])
        self.assertIn(self.hypotheses[0].content.split()[0], merged.content)
        self.assertIn(self.hypotheses[1].content.split()[-1], merged.content)
        self.assertEqual(merged.metadata['operation'], 'merge')

    def test_prune_reduces_population(self):
        pruned = self.evolver.prune(self.hypotheses, self.scores, keep_ratio=0.5)
        self.assertEqual(len(pruned), 1)

    def test_evolve_returns_population(self):
        evolved = self.evolver.evolve(self.hypotheses, self.scores, target_population=3)
        self.assertEqual(len(evolved), 3)


if __name__ == '__main__':
    unittest.main()
