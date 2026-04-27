"""
Constraints: Risk thresholds and safety enforcement for Kairoseed.
"""

from typing import Dict, Any, List, Optional
from models.hypothesis import Hypothesis, HypothesisEvaluation


class SafetyConstraints:
    """
    Enforces safety constraints and thresholds on hypotheses and decisions.

    Implements risk thresholds (τ) and quality thresholds (θ).
    """

    def __init__(self, risk_threshold: float = 0.7, quality_threshold: float = 0.3,
                 max_cost: float = 0.8, min_stability: float = 0.2):
        self.risk_threshold = risk_threshold      # τ - maximum allowed risk
        self.quality_threshold = quality_threshold  # θ - minimum required score
        self.max_cost = max_cost                  # Maximum allowed cost
        self.min_stability = min_stability        # Minimum required stability

    def check_hypothesis_constraints(self, hypothesis: Hypothesis,
                                   evaluation: HypothesisEvaluation) -> Dict[str, Any]:
        """
        Check if a hypothesis meets all safety constraints.

        Args:
            hypothesis: The hypothesis to check
            evaluation: Its evaluation results

        Returns:
            Dict with 'passed': bool and violation details
        """
        violations = []

        # Risk threshold check
        if evaluation.risk > self.risk_threshold:
            violations.append({
                'type': 'risk_threshold',
                'value': evaluation.risk,
                'threshold': self.risk_threshold,
                'message': f'Risk {evaluation.risk:.2f} exceeds threshold {self.risk_threshold}'
            })

        # Quality threshold check
        if evaluation.score < self.quality_threshold:
            violations.append({
                'type': 'quality_threshold',
                'value': evaluation.score,
                'threshold': self.quality_threshold,
                'message': f'Score {evaluation.score:.2f} below threshold {self.quality_threshold}'
            })

        # Cost constraint
        if evaluation.cost > self.max_cost:
            violations.append({
                'type': 'max_cost',
                'value': evaluation.cost,
                'threshold': self.max_cost,
                'message': f'Cost {evaluation.cost:.2f} exceeds maximum {self.max_cost}'
            })

        # Stability constraint
        if evaluation.stability < self.min_stability:
            violations.append({
                'type': 'min_stability',
                'value': evaluation.stability,
                'threshold': self.min_stability,
                'message': f'Stability {evaluation.stability:.2f} below minimum {self.min_stability}'
            })

        return {
            'passed': len(violations) == 0,
            'violations': violations,
            'constraint_check': True
        }

    def filter_hypotheses(self, hypotheses: List[Hypothesis],
                         evaluations: List[HypothesisEvaluation]) -> List[Hypothesis]:
        """
        Filter hypotheses that don't meet constraints.

        Args:
            hypotheses: List of hypotheses
            evaluations: Corresponding evaluations

        Returns:
            List of hypotheses that pass constraints
        """
        filtered = []
        for hyp, eval in zip(hypotheses, evaluations):
            check = self.check_hypothesis_constraints(hyp, eval)
            if check['passed']:
                filtered.append(hyp)

        return filtered

    def get_constraint_summary(self, hypotheses: List[Hypothesis],
                             evaluations: List[HypothesisEvaluation]) -> Dict[str, Any]:
        """
        Get summary of constraint violations across a set of hypotheses.
        """
        total = len(hypotheses)
        passed = 0
        violations_by_type = {}

        for hyp, eval in zip(hypotheses, evaluations):
            check = self.check_hypothesis_constraints(hyp, eval)
            if check['passed']:
                passed += 1
            else:
                for violation in check['violations']:
                    v_type = violation['type']
                    if v_type not in violations_by_type:
                        violations_by_type[v_type] = 0
                    violations_by_type[v_type] += 1

        return {
            'total_hypotheses': total,
            'passed_constraints': passed,
            'failed_constraints': total - passed,
            'pass_rate': passed / total if total > 0 else 0,
            'violations_by_type': violations_by_type
        }

    def adjust_thresholds(self, feedback: Dict[str, float]):
        """
        Adjust constraint thresholds based on feedback.

        Args:
            feedback: Dict with adjustment factors for each threshold
        """
        if 'risk_threshold' in feedback:
            self.risk_threshold = max(0.0, min(1.0,
                self.risk_threshold * feedback['risk_threshold']))

        if 'quality_threshold' in feedback:
            self.quality_threshold = max(0.0, min(1.0,
                self.quality_threshold * feedback['quality_threshold']))

        if 'max_cost' in feedback:
            self.max_cost = max(0.0, min(1.0,
                self.max_cost * feedback['max_cost']))

        if 'min_stability' in feedback:
            self.min_stability = max(0.0, min(1.0,
                self.min_stability * feedback['min_stability']))


class AdaptiveConstraints(SafetyConstraints):
    """
    Constraints that adapt based on system performance and outcomes.
    """

    def __init__(self, *args, adaptation_rate: float = 0.1, **kwargs):
        super().__init__(*args, **kwargs)
        self.adaptation_rate = adaptation_rate
        self.performance_history = []

    def learn_from_outcome(self, outcome: Dict[str, Any]):
        """
        Learn from decision outcomes to adjust constraints.

        Args:
            outcome: Dict with 'success': bool, 'actual_risk': float, etc.
        """
        self.performance_history.append(outcome)

        if len(self.performance_history) < 5:
            return  # Need minimum history

        recent = self.performance_history[-10:]  # Last 10 outcomes

        # Calculate recent success rate
        success_rate = sum(1 for o in recent if o.get('success', False)) / len(recent)

        # Adjust thresholds based on performance
        if success_rate > 0.8:
            # Too conservative - relax constraints slightly
            self.risk_threshold = min(1.0, self.risk_threshold + self.adaptation_rate * 0.1)
            self.quality_threshold = max(0.0, self.quality_threshold - self.adaptation_rate * 0.05)

        elif success_rate < 0.3:
            # Too risky - tighten constraints
            self.risk_threshold = max(0.0, self.risk_threshold - self.adaptation_rate * 0.1)
            self.quality_threshold = min(1.0, self.quality_threshold + self.adaptation_rate * 0.05)

        # Adjust based on actual vs predicted risk
        avg_predicted_risk = sum(o.get('predicted_risk', 0) for o in recent) / len(recent)
        avg_actual_risk = sum(o.get('actual_risk', 0) for o in recent) / len(recent)

        risk_error = avg_actual_risk - avg_predicted_risk
        if abs(risk_error) > 0.2:
            # Risk prediction is off - adjust threshold
            adjustment = self.adaptation_rate * risk_error
            self.risk_threshold = max(0.0, min(1.0, self.risk_threshold + adjustment))