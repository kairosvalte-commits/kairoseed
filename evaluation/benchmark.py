"""
Benchmarking module for Kairoseed evaluation metrics.

Provides simple performance baselines for scoring and evolution components.
"""

from typing import Dict, Any
import time
from core.kairoseed import Kairoseed
from core.gsbs import GSBS
from core.pee import PEE


class Benchmark:
    """Run benchmarking experiments for Kairoseed components."""

    def __init__(self, num_runs: int = 50):
        self.num_runs = num_runs

    def run(self, input_state: str) -> Dict[str, Any]:
        start = time.perf_counter()
        generator = Kairoseed(num_hypotheses=5)
        hypotheses = generator.generate_hypotheses(input_state)

        scorer = GSBS()
        scores = scorer.score_hypotheses(hypotheses)

        evolver = PEE()
        evolved = evolver.evolve(hypotheses, scores, target_population=5)

        duration = time.perf_counter() - start
        return {
            "input_state": input_state,
            "hypothesis_count": len(hypotheses),
            "evolved_count": len(evolved),
            "duration_seconds": duration
        }

    def profile(self) -> None:
        for case in ["study coding daily", "optimize planning", "learn new skill"]:
            result = self.run(case)
            print(f"Benchmark {case}: {result['duration_seconds']:.4f}s")


if __name__ == "__main__":
    Benchmark().profile()
