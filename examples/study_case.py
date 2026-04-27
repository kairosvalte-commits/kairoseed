"""
Study Case Example: Using Kairoseed for learning strategy optimization.

Demonstrates the full pipeline with a practical example.
"""

from core.pipeline import KairoseedPipeline
from safety.agt_interface import create_agt_interface


def run_study_case():
    """
    Run the study case example: optimizing daily coding study habits.
    """
    print("🧠 Kairoseed Study Case: Optimizing Daily Coding Study")
    print("=" * 60)

    # Initialize pipeline
    pipeline = KairoseedPipeline(
        num_hypotheses=4,
        evolution_iterations=2
    )

    # Input: learning goal
    input_state = "study coding daily to improve programming skills"

    print(f"Input: {input_state}")
    print()

    # Run without AGT (basic mode)
    print("🚀 Running Kairoseed Pipeline (Basic Mode)")
    result = pipeline.run(input_state, use_evolution=True)

    print("\n📦 Decision Result:")
    print(f"Selected: {result.decision}")
    print(f"Result: {result.result}")
    print(f"Memory Updated: {result.memory_updated}")

    # Run with AGT safety gate
    print("\n🛡️ Running with AGT Safety Gate")
    agt = create_agt_interface("basic", risk_threshold=0.8)
    result_with_agt = pipeline.run_with_agt(input_state, agt_gate=lambda h: True)  # Mock approval

    print(f"AGT Approved: {result_with_agt.decision != 'Blocked by AGT safety gate'}")
    print(f"Final Decision: {result_with_agt.decision}")

    return result


def run_multiple_cases():
    """
    Run multiple study cases to demonstrate learning.
    """
    print("🔄 Multiple Study Cases - Demonstrating Learning")
    print("=" * 60)

    pipeline = KairoseedPipeline(num_hypotheses=3, evolution_iterations=1)

    cases = [
        "study coding daily",
        "learn machine learning",
        "improve problem solving",
        "practice algorithms",
        "build projects"
    ]

    for case in cases:
        print(f"\nCase: {case}")
        result = pipeline.run(case, use_evolution=False)  # Quick mode
        print(f"Decision: {result.decision}")


if __name__ == "__main__":
    # Run single case
    result = run_study_case()

    print("\n" + "=" * 60)
    print("Example completed. Check memory/store.json for learned weights.")

    # Uncomment to run multiple cases
    # run_multiple_cases()