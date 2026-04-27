from evaluation.benchmarks.stability_benchmark import run_stability_test
from evaluation.benchmarks.memory_drift_benchmark import run_memory_drift_test
from evaluation.benchmarks.evolution_gain_benchmark import run_evolution_gain_test

def run_all_benchmarks(input_state):
    return {
        "stability": run_stability_test(input_state),
        "memory_drift": run_memory_drift_test(input_state),
        "evolution_gain": run_evolution_gain_test(input_state)
    }