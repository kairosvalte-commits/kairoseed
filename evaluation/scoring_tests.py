"""
Scoring tests for the evaluation layer.

Provides lightweight validation routines for GSBS scoring behavior.
"""

from core.gsbs import GSBS
from models.hypothesis import Hypothesis


def run_scoring_check():
    scorer = GSBS()
    hypotheses = [Hypothesis.create("score test 1"), Hypothesis.create("score test 2")]
    scores = scorer.score_hypotheses(hypotheses)
    return all(hasattr(score, 'score') for score in scores)


if __name__ == "__main__":
    result = run_scoring_check()
    print(f"Scoring tests pass: {result}")
