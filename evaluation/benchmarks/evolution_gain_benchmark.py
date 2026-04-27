from core.pipeline import run_pipeline

def run_evolution_gain_test(input_state):
    result = run_pipeline(input_state)

    h_initial = result["initial_hypothesis"]
    h_final = result["selected_hypothesis"]

    return {
        "initial": h_initial,
        "final": h_final,
        "gain": h_final["score"] - h_initial["score"]
    }