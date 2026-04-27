"""
GSBS: Generalized Scoring and Selection System

Scores hypotheses using weighted evaluation of success, stability, cost, and risk.
"""

from typing import List, Dict, Any, Tuple
import random


class HypothesisScore:
    def __init__(self, hypothesis_id: str, success: float, stability: float,
                 cost: float, risk: float, weights: Dict[str, float] = None):
        self.hypothesis_id = hypothesis_id
        self.success = success  # 0-1, higher better
        self.stability = stability  # 0-1, higher better
        self.cost = cost  # 0-1, higher worse (normalized cost)
        self.risk = risk  # 0-1, higher worse
        self.weights = weights or {
            'success': 0.4,
            'stability': 0.3,
            'cost': 0.2,
            'risk': 0.1
        }

    @property
    def score(self) -> float:
        """Calculate weighted score for the hypothesis."""
        return (self.weights['success'] * self.success +
                self.weights['stability'] * self.stability -
                self.weights['cost'] * self.cost -
                self.weights['risk'] * self.risk)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'hypothesis_id': self.hypothesis_id,
            'success': self.success,
            'stability': self.stability,
            'cost': self.cost,
            'risk': self.risk,
            'score': self.score,
            'weights': self.weights
        }


class GSBS:
    """
    Generalized Scoring and Selection System.
    Evaluates hypotheses and selects the optimal one.
    """

    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            'success': 0.4,
            'stability': 0.3,
            'cost': 0.2,
            'risk': 0.1
        }

    def evaluate_hypothesis(self, hypothesis) -> HypothesisScore:
        """
        Evaluate a single hypothesis.
        In practice, this would use models or heuristics to assess each dimension.

        Args:
            hypothesis: Hypothesis object with id and content

        Returns:
            HypothesisScore with evaluation
        """
        # Basic implementation - random evaluation
        # In real system, this would analyze hypothesis content
        success = random.uniform(0.1, 0.9)
        stability = random.uniform(0.1, 0.9)
        cost = random.uniform(0.1, 0.9)
        risk = random.uniform(0.1, 0.9)

        return HypothesisScore(
            hypothesis_id=hypothesis.id,
            success=success,
            stability=stability,
            cost=cost,
            risk=risk,
            weights=self.weights
        )

    def score_hypotheses(self, hypotheses: List) -> List[HypothesisScore]:
        """
        Score a list of hypotheses.

        Args:
            hypotheses: List of hypothesis objects

        Returns:
            List of HypothesisScore objects
        """
        scores = []
        for hyp in hypotheses:
            score = self.evaluate_hypothesis(hyp)
            scores.append(score)
        return scores

    def select_best(self, hypotheses: List, scores: List[HypothesisScore] = None) -> Tuple[Any, HypothesisScore]:
        """
        Select the hypothesis with the highest score.

        Args:
            hypotheses: List of hypothesis objects
            scores: Pre-computed scores (optional)

        Returns:
            Tuple of (selected_hypothesis, its_score)
        """
        if scores is None:
            scores = self.score_hypotheses(hypotheses)

        if not scores:
            return None, None

        best_score = max(scores, key=lambda s: s.score)
        best_hyp = next(h for h in hypotheses if h.id == best_score.hypothesis_id)

        return best_hyp, best_score

    def update_weights(self, feedback: Dict[str, float]):
        """
        Update scoring weights based on feedback.

        Args:
            feedback: Dict with weight adjustments
        """
        for key, adjustment in feedback.items():
            if key in self.weights:
                self.weights[key] = max(0.0, min(1.0, self.weights[key] + adjustment))


# Example usage
if __name__ == "__main__":
    from kairoseed import Kairoseed

    # Generate hypotheses
    generator = Kairoseed(3)
    hyps = generator.generate_hypotheses("learn machine learning")

    # Score them
    scorer = GSBS()
    scores = scorer.score_hypotheses(hyps)

    # Select best
    best_hyp, best_score = scorer.select_best(hyps, scores)

    print("Hypotheses and Scores:")
    for hyp, score in zip(hyps, scores):
        print(f"{hyp.id}: {hyp.content} -> Score: {score.score:.3f}")

    print(f"\nBest: {best_hyp.content} (Score: {best_score.score:.3f})")