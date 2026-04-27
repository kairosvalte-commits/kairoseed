"""
Decision Compiler: Translate selected hypotheses into executable decision artifacts.

This module is part of the v0.4 upgrade and bridges selected hypotheses
with structured decision outputs.
"""

from typing import Any, Dict
from models.decision import Decision


class DecisionCompiler:
    """Compile selected hypotheses into decision payloads."""

    def __init__(self, compiler_name: str = "v0.4-compiler"):
        self.compiler_name = compiler_name

    def compile(self, hypothesis: Any, input_state: str, score: float) -> Decision:
        """Compile the selected hypothesis into a structured decision object."""
        decision_text = f"Execute: {hypothesis.content}"
        decision = Decision(
            input_state=input_state,
            selected_hypothesis=hypothesis,
            decision_text=decision_text,
            confidence_score=score,
            execution_status="compiled",
            result=None,
            metadata={
                "compiler": self.compiler_name,
                "compiled_at": "v0.4"
            }
        )
        return decision

    def summarize(self, decision: Decision) -> Dict[str, Any]:
        """Return a lightweight summary of the compiled decision."""
        return {
            "id": decision.selected_hypothesis.id,
            "decision_text": decision.decision_text,
            "confidence_score": decision.confidence_score,
            "status": decision.execution_status,
            "compiler": self.compiler_name
        }


if __name__ == "__main__":
    from models.hypothesis import Hypothesis

    example_hyp = Hypothesis.create("Test compile decision")
    compiler = DecisionCompiler()
    compiled = compiler.compile(example_hyp, "test input", score=0.72)
    print(compiled.to_dict())
