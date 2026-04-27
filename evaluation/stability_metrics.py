"""
Stability metrics for Kairoseed evaluation.

Measures hypothesis stability and drift across iterations.
"""

from typing import List, Dict


def compute_stability(scores: List[float]) -> float:
    """Compute a simple stability metric for a sequence of scores."""
    if not scores:
        return 0.0
    mean = sum(scores) / len(scores)
    variance = sum((s - mean) ** 2 for s in scores) / len(scores)
    return max(0.0, 1.0 - variance)


def identify_drift(history: List[Dict[str, float]]) -> Dict[str, float]:
    """Detect drift in evaluation metrics over time."""
    if not history:
        return {"drift": 0.0, "direction": "stable"}

    baseline = history[0]
    latest = history[-1]
    drift = 0.0
    for key in ["success", "stability", "cost", "risk"]:
        drift += abs(latest.get(key, 0.0) - baseline.get(key, 0.0))

    drift = drift / 4.0
    direction = "improving" if latest.get("success", 0.0) >= baseline.get("success", 0.0) else "declining"
    return {"drift": drift, "direction": direction}
