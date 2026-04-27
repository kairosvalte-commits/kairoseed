"""
Vector Model: GSBS vector representation for hypothesis evaluation.

Defines the vector representation used in the v0.4 GSBS scoring layer.
"""

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class HypothesisVector:
    """Vector representation of hypothesis properties."""
    success: float
    stability: float
    cost: float
    risk: float

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)

    def normalize(self) -> "HypothesisVector":
        """Normalize vector components to [0, 1]."""
        components = [self.success, self.stability, self.cost, self.risk]
        min_val = min(components)
        max_val = max(components)
        if max_val - min_val == 0:
            return self
        return HypothesisVector(
            success=(self.success - min_val) / (max_val - min_val),
            stability=(self.stability - min_val) / (max_val - min_val),
            cost=(self.cost - min_val) / (max_val - min_val),
            risk=(self.risk - min_val) / (max_val - min_val)
        )

    def score(self, weights: Dict[str, float]) -> float:
        """Compute a weighted score for the vector."""
        return (
            weights.get("success", 0.0) * self.success +
            weights.get("stability", 0.0) * self.stability -
            weights.get("cost", 0.0) * self.cost -
            weights.get("risk", 0.0) * self.risk
        )
