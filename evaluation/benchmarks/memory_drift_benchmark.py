from core.pipeline import run_pipeline

def run_memory_drift_test(input_state, runs=5):
    memories = []

    state = input_state

    for _ in range(runs):
        result = run_pipeline(state)
        memories.append(result["memory_snapshot"])
        state = input_state  # same input each time

    return {
        "drift_detected": len(set(str(m) for m in memories)) > 1,
        "memory_states": memories
    }