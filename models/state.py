"""
State Model: System state container for Kairoseed pipeline.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from .hypothesis import Hypothesis, HypothesisEvaluation


@dataclass
class SystemState:
    """
    Container for the current state of the Kairoseed system.

    Tracks the evolution of hypotheses through the pipeline.
    """
    input_state: str
    current_hypotheses: List[Hypothesis] = field(default_factory=list)
    evaluations: List[HypothesisEvaluation] = field(default_factory=list)
    selected_hypothesis: Optional[Hypothesis] = None
    iteration: int = 0
    weights: Dict[str, float] = field(default_factory=lambda: {
        'success': 0.4,
        'stability': 0.3,
        'cost': 0.2,
        'risk': 0.1
    })
    memory: Dict[str, Any] = field(default_factory=dict)

    def add_hypothesis(self, hypothesis: Hypothesis):
        """Add a hypothesis to the current set."""
        self.current_hypotheses.append(hypothesis)

    def add_evaluation(self, evaluation: HypothesisEvaluation):
        """Add an evaluation result."""
        self.evaluations.append(evaluation)

    def select_hypothesis(self, hypothesis: Hypothesis):
        """Mark a hypothesis as selected."""
        self.selected_hypothesis = hypothesis

    def advance_iteration(self):
        """Move to next evolution iteration."""
        self.iteration += 1
        # Could update weights or other state here

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary."""
        return {
            'input_state': self.input_state,
            'current_hypotheses': [h.to_dict() for h in self.current_hypotheses],
            'evaluations': [e.to_dict() for e in self.evaluations],
            'selected_hypothesis': self.selected_hypothesis.to_dict() if self.selected_hypothesis else None,
            'iteration': self.iteration,
            'weights': self.weights,
            'memory': self.memory
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SystemState':
        """Create state from dictionary."""
        # Reconstruct hypotheses and evaluations
        hypotheses = [Hypothesis.from_dict(h) for h in data.get('current_hypotheses', [])]
        evaluations = [HypothesisEvaluation(**e) for e in data.get('evaluations', [])]

        selected = None
        if data.get('selected_hypothesis'):
            selected = Hypothesis.from_dict(data['selected_hypothesis'])

        return cls(
            input_state=data['input_state'],
            current_hypotheses=hypotheses,
            evaluations=evaluations,
            selected_hypothesis=selected,
            iteration=data.get('iteration', 0),
            weights=data.get('weights', {}),
            memory=data.get('memory', {})
        )