"""
Hypothesis Model: Data structure for hypotheses in Kairoseed system.
"""

from typing import Dict, Any, Optional
import uuid
from dataclasses import dataclass, asdict


@dataclass
class Hypothesis:
    """
    Represents a hypothesis in the Kairoseed system.

    A hypothesis is a candidate solution or strategy for a given input state.
    """
    id: str
    content: str
    metadata: Dict[str, Any]
    score: Optional[float] = None
    generation: int = 0  # Evolution generation

    @classmethod
    def create(cls, content: str, metadata: Dict[str, Any] = None,
               generation: int = 0) -> 'Hypothesis':
        """Create a new hypothesis with auto-generated ID."""
        return cls(
            id=str(uuid.uuid4())[:8],
            content=content,
            metadata=metadata or {},
            generation=generation
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Hypothesis':
        """Create hypothesis from dictionary."""
        return cls(**data)

    def __str__(self) -> str:
        return f"Hypothesis({self.id}): {self.content}"


@dataclass
class HypothesisEvaluation:
    """
    Evaluation results for a hypothesis.
    """
    hypothesis_id: str
    success: float  # 0-1
    stability: float  # 0-1
    cost: float  # 0-1 (normalized)
    risk: float  # 0-1
    score: float
    weights: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)