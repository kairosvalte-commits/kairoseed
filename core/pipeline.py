"""
Pipeline: Full Kairoseed Loop Orchestration

Orchestrates the complete decision evolution pipeline.
"""

from typing import Dict, Any, Optional, List
import json
from .kairoseed import Kairoseed
from .gsbs import GSBS
from .pee import PEE


class PipelineResult:
    def __init__(self, input_state: str, selected_hypothesis: Any,
                 decision: str, result: str, memory_updated: bool = False, selected_score: Any = None):
        self.input_state = input_state
        self.selected_hypothesis = selected_hypothesis
        self.decision = decision
        self.result = result
        self.memory_updated = memory_updated
        self.selected_score = selected_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input": self.input_state,
            "selected": self.selected_hypothesis.id if self.selected_hypothesis else None,
            "decision": self.decision,
            "result": self.result,
            "memory_update": self.memory_updated,
            "selected_score": self.selected_score.score if self.selected_score else None
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class KairoseedPipeline:
    """
    Complete Kairoseed decision evolution pipeline.
    Orchestrates hypothesis generation, evaluation, evolution, and selection.
    """

    def __init__(self, num_hypotheses: int = 5, evolution_iterations: int = 2):
        self.num_hypotheses = num_hypotheses
        self.evolution_iterations = evolution_iterations

        # Initialize components
        self.generator = Kairoseed(num_hypotheses)
        self.scorer = GSBS()
        self.evolver = PEE()

    def run(self, input_state: str, use_evolution: bool = True) -> PipelineResult:
        """
        Execute the full Kairoseed pipeline.

        Args:
            input_state: Input problem or situation description
            use_evolution: Whether to apply PEE evolution

        Returns:
            PipelineResult with decision outcome
        """
        print(f"🔄 Processing input: {input_state}")

        # Step 1: Generate initial hypotheses
        print("🧠 Generating hypotheses...")
        hypotheses = self.generator.generate_hypotheses(input_state)

        # Step 2: Score hypotheses
        print("📊 Scoring hypotheses...")
        scores = self.scorer.score_hypotheses(hypotheses)

        # Print initial results
        for hyp, score in zip(hypotheses, scores):
            print(f"  {hyp.id}: {hyp.content} -> Score: {score.score:.3f}")

        # Step 3: Evolution loop (optional)
        if use_evolution:
            print("🧬 Evolving hypotheses...")
            for iteration in range(self.evolution_iterations):
                print(f"  Iteration {iteration + 1}...")
                hypotheses = self.evolver.evolve(hypotheses, scores, self.num_hypotheses)
                scores = self.scorer.score_hypotheses(hypotheses)

                for hyp, score in zip(hypotheses, scores):
                    print(f"    {hyp.id}: {hyp.content} -> Score: {score.score:.3f}")

        # Step 4: Select best hypothesis
        print("🎯 Selecting best hypothesis...")
        best_hyp, best_score = self.scorer.select_best(hypotheses, scores)

        if best_hyp:
            print(f"Selected: {best_hyp.content} (Score: {best_score.score:.3f})")
            decision = best_hyp.content
            result = f"Selected hypothesis with score {best_score.score:.3f}"
        else:
            decision = "No suitable hypothesis found"
            result = "Pipeline failed to select hypothesis"

        # Step 5: Memory update (placeholder)
        memory_updated = True  # In real system, would check if weights changed

        return PipelineResult(
            input_state=input_state,
            selected_hypothesis=best_hyp,
            decision=decision,
            result=result,
            memory_updated=memory_updated,
            selected_score=best_score
        )

    def run_with_agt(self, input_state: str, agt_gate=None) -> PipelineResult:
        """
        Run pipeline with optional AGT safety gate.

        Args:
            input_state: Input state
            agt_gate: Optional safety gate function

        Returns:
            PipelineResult
        """
        result = self.run(input_state)

        if agt_gate and result.selected_hypothesis:
            # Apply AGT gate
            approved = agt_gate(result.selected_hypothesis)
            if not approved:
                result.decision = "Blocked by AGT safety gate"
                result.result = "Hypothesis rejected for safety reasons"

        return result


# Example usage
if __name__ == "__main__":
    pipeline = KairoseedPipeline(num_hypotheses=3, evolution_iterations=1)

    result = pipeline.run("study coding daily")

    print("\n📦 Final Result:")
    print(result.to_json())


def run_pipeline(input_state: str) -> Dict[str, Any]:
    """
    Convenience function to run the pipeline and return a dict with benchmark-compatible keys.
    """
    pipeline = KairoseedPipeline()
    result = pipeline.run(input_state)

    # Get initial hypothesis (first one before evolution)
    initial_hypotheses = pipeline.generator.generate_hypotheses(input_state)
    initial_scores = pipeline.scorer.score_hypotheses(initial_hypotheses)
    initial_best = pipeline.scorer.select_best(initial_hypotheses, initial_scores)

    return {
        "decision": result.decision,
        "memory_snapshot": {"placeholder": "memory_state"},  # Placeholder for actual memory
        "initial_hypothesis": {
            "content": initial_best[0].content if initial_best[0] else None,
            "score": initial_best[1].score if initial_best[1] else 0.0
        } if initial_best[0] else {"content": None, "score": 0.0},
        "selected_hypothesis": {
            "content": result.selected_hypothesis.content if result.selected_hypothesis else None,
            "score": result.selected_score.score if result.selected_score else 0.0
        } if result.selected_hypothesis else {"content": None, "score": 0.0}
    }