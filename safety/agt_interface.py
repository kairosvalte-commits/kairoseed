"""
AGT Interface: Optional safety boundary layer for Kairoseed.

AGT (Autonomous Governance Technology) acts as a permission gate
and risk filter for hypothesis execution.
"""

from typing import Dict, Any, Optional, Callable, List
from abc import ABC, abstractmethod
from models.hypothesis import Hypothesis


class AGTInterface(ABC):
    """
    Abstract base class for AGT safety interfaces.

    AGT provides external validation and safety checking for decisions.
    """

    @abstractmethod
    def validate_hypothesis(self, hypothesis: Hypothesis) -> Dict[str, Any]:
        """
        Validate a hypothesis for safety and compliance.

        Returns:
            Dict with 'approved': bool and optional 'reason': str
        """
        pass

    @abstractmethod
    def check_risk_threshold(self, risk_score: float, threshold: float = 0.7) -> bool:
        """
        Check if risk score exceeds safety threshold.

        Returns:
            True if safe (below threshold), False if too risky
        """
        pass


class BasicAGT(AGTInterface):
    """
    Basic implementation of AGT with rule-based safety checks.
    """

    def __init__(self, risk_threshold: float = 0.7, banned_keywords: List[str] = None):
        self.risk_threshold = risk_threshold
        self.banned_keywords = banned_keywords or [
            'dangerous', 'harmful', 'illegal', 'unsafe'
        ]

    def validate_hypothesis(self, hypothesis: Hypothesis) -> Dict[str, Any]:
        """
        Basic validation: check for banned keywords and risk score.
        """
        content = hypothesis.content.lower()

        # Check for banned keywords
        for keyword in self.banned_keywords:
            if keyword in content:
                return {
                    'approved': False,
                    'reason': f'Contains banned keyword: {keyword}'
                }

        # Check risk score if available
        if hasattr(hypothesis, 'risk') and hypothesis.risk > self.risk_threshold:
            return {
                'approved': False,
                'reason': f'Risk score {hypothesis.risk:.2f} exceeds threshold {self.risk_threshold}'
            }

        return {
            'approved': True,
            'reason': 'Passed basic safety checks'
        }

    def check_risk_threshold(self, risk_score: float, threshold: float = None) -> bool:
        """Check risk against threshold."""
        threshold = threshold or self.risk_threshold
        return risk_score <= threshold


class MockAGT(AGTInterface):
    """
    Mock AGT that always approves - for testing without safety constraints.
    """

    def validate_hypothesis(self, hypothesis: Hypothesis) -> Dict[str, Any]:
        return {
            'approved': True,
            'reason': 'Mock AGT - always approved'
        }

    def check_risk_threshold(self, risk_score: float, threshold: float = 0.7) -> bool:
        return True


class StrictAGT(AGTInterface):
    """
    Strict AGT that requires explicit approval for high-risk actions.
    """

    def __init__(self, risk_threshold: float = 0.5, require_human_approval: bool = True):
        self.risk_threshold = risk_threshold
        self.require_human_approval = require_human_approval

    def validate_hypothesis(self, hypothesis: Hypothesis) -> Dict[str, Any]:
        # Always require approval for now (simplified)
        if self.require_human_approval:
            return {
                'approved': False,
                'reason': 'Human approval required',
                'requires_human': True
            }

        return {
            'approved': True,
            'reason': 'Passed strict validation'
        }

    def check_risk_threshold(self, risk_score: float, threshold: float = None) -> bool:
        threshold = threshold or self.risk_threshold
        return risk_score <= threshold


def create_agt_interface(agt_type: str = "basic", **kwargs) -> AGTInterface:
    """
    Factory function to create AGT interfaces.

    Args:
        agt_type: Type of AGT ('basic', 'mock', 'strict')
        **kwargs: Additional parameters for AGT initialization

    Returns:
        AGTInterface instance
    """
    if agt_type == "basic":
        return BasicAGT(**kwargs)
    elif agt_type == "mock":
        return MockAGT(**kwargs)
    elif agt_type == "strict":
        return StrictAGT(**kwargs)
    else:
        raise ValueError(f"Unknown AGT type: {agt_type}")


# Convenience function for pipeline integration
def agt_gate(hypothesis: Hypothesis, agt: Optional[AGTInterface] = None) -> bool:
    """
    Convenience function to check hypothesis against AGT.

    Returns:
        True if approved, False if blocked
    """
    if agt is None:
        agt = MockAGT()  # Default to permissive

    result = agt.validate_hypothesis(hypothesis)
    return result.get('approved', False)