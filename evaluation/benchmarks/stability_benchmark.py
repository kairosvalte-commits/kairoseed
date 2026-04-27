from core.pipeline import run_pipeline

def run_stability_test(input_state, runs=5):
    outputs = []

    for _ in range(runs):
        result = run_pipeline(input_state)
        outputs.append(result["decision"])

    stable = len(set(outputs)) == 1

    return {
        "stable": stable,
        "outputs": outputs
    }