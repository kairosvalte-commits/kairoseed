"""
Memory Learning Demo: Show how the Kairoseed memory system updates weights.
"""

from core.pipeline import KairoseedPipeline
from core.compiler import DecisionCompiler
from memory.memory import Memory


def run_memory_demo():
    pipeline = KairoseedPipeline(num_hypotheses=3, evolution_iterations=1)
    compiler = DecisionCompiler()
    memory = Memory(storage_path="memory/store.json")

    result = pipeline.run("learn from feedback", use_evolution=False)
    compiled_decision = compiler.compile(result.selected_hypothesis, result.input_state, score=0.8)
    memory.store_decision(compiled_decision)
    memory.update_weights(predicted_score=0.5, actual_outcome=0.8)

    print("Memory weights:")
    print(memory.get_weights())
    print("Recent weight history:")
    print(memory.get_weight_evolution())


if __name__ == "__main__":
    run_memory_demo()
