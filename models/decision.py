"""
Decision Model: Output schema for selected hypotheses and decisions.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from .hypothesis import Hypothesis


@dataclass
class Decision:
    """
    Represents a decision made by the Kairoseed system.

    Contains the selected hypothesis and execution details.
    """
    input_state: str
    selected_hypothesis: Hypothesis
    decision_text: str
    confidence_score: float
    execution_status: str = "pending"  # pending, executing, completed, failed
    result: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'input_state': self.input_state,
            'selected_hypothesis': self.selected_hypothesis.to_dict(),
            'decision_text': self.decision_text,
            'confidence_score': self.confidence_score,
            'execution_status': self.execution_status,
            'result': self.result,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Decision':
        """Create from dictionary."""
        hyp_data = data['selected_hypothesis']
        selected = Hypothesis.from_dict(hyp_data)

        return cls(
            input_state=data['input_state'],
            selected_hypothesis=selected,
            decision_text=data['decision_text'],
            confidence_score=data['confidence_score'],
            execution_status=data.get('execution_status', 'pending'),
            result=data.get('result'),
            timestamp=datetime.fromisoformat(data['timestamp']),
            metadata=data.get('metadata', {})
        )

    def mark_executed(self, result: str):
        """Mark decision as executed with result."""
        self.execution_status = "completed"
        self.result = result
        self.timestamp = datetime.now()

    def mark_failed(self, error: str):
        """Mark decision as failed."""
        self.execution_status = "failed"
        self.result = error
        self.timestamp = datetime.now()


@dataclass
class DecisionHistory:
    """
    Tracks history of decisions for learning and analysis.
    """
    decisions: List[Decision] = field(default_factory=list)

    def add_decision(self, decision: Decision):
        """Add a decision to history."""
        self.decisions.append(decision)

    def get_recent_decisions(self, limit: int = 10) -> List[Decision]:
        """Get most recent decisions."""
        return sorted(self.decisions, key=lambda d: d.timestamp, reverse=True)[:limit]

    def get_success_rate(self) -> float:
        """Calculate success rate of executed decisions."""
        executed = [d for d in self.decisions if d.execution_status in ['completed', 'failed']]
        if not executed:
            return 0.0
        successful = [d for d in executed if d.execution_status == 'completed']
        return len(successful) / len(executed)