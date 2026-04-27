"""
Decision Demo: Showcase the compiler and pipeline integration.
"""

from core.pipeline import KairoseedPipeline
from core.compiler import DecisionCompiler


def run_demo():
    pipeline = KairoseedPipeline(num_hypotheses=4, evolution_iterations=1)
    result = pipeline.run("optimize daily workflow", use_evolution=True)

    compiler = DecisionCompiler()
    compiled = compiler.compile(result.selected_hypothesis, result.input_state, score=0.75)

    print("Compiled Decision:")
    print(compiled.to_dict())


if __name__ == "__main__":
    run_demo()
