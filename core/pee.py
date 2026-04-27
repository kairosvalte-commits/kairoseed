"""
PEE: Prediction Error Evolution Engine

Evolves hypotheses through mutation, merging, and pruning operations.
"""

from typing import List, Dict, Any, Optional
import random
import copy
from .gsbs import HypothesisScore


class PEE:
    """
    Prediction Error Evolution Engine.
    Evolves hypothesis space through genetic operations.
    """

    def __init__(self, mutation_rate: float = 0.1, novelty_threshold: float = 0.1):
        self.mutation_rate = mutation_rate
        self.novelty_threshold = novelty_threshold

    def mutate(self, hypothesis, mutation_strength: float = 0.1) -> Any:
        """
        Mutate a hypothesis by introducing small changes.

        Args:
            hypothesis: Original hypothesis object
            mutation_strength: How much to mutate (0-1)

        Returns:
            Mutated hypothesis
        """
        # Basic text mutation - in practice, this would be more sophisticated
        content = hypothesis.content

        # Simple mutation: add/remove/replace words
        words = content.split()
        if random.random() < self.mutation_rate and len(words) > 1:
            # Replace a random word with a synonym or variation
            idx = random.randint(0, len(words) - 1)
            original_word = words[idx]

            # Simple variations
            variations = {
                'direct': ['straightforward', 'immediate'],
                'conservative': ['cautious', 'safe'],
                'aggressive': ['intensive', 'bold'],
                'long-term': ['sustained', 'extended'],
                'minimal': ['basic', 'simple']
            }

            if original_word.lower() in variations:
                words[idx] = random.choice(variations[original_word.lower()])
            else:
                # Add modifier
                modifiers = ['improved', 'enhanced', 'optimized', 'refined']
                words.insert(idx, random.choice(modifiers))

            content = ' '.join(words)

        # Create new hypothesis with mutated content
        mutated = copy.deepcopy(hypothesis)
        mutated.content = content
        mutated.id = f"{hypothesis.id}_mut"
        mutated.metadata = hypothesis.metadata.copy()
        mutated.metadata['operation'] = 'mutation'

        return mutated

    def merge(self, hyp1, hyp2) -> Any:
        """
        Merge two hypotheses into a hybrid.

        Args:
            hyp1, hyp2: Hypothesis objects to merge

        Returns:
            Merged hypothesis
        """
        # Simple merge: combine contents
        content1 = hyp1.content.split()
        content2 = hyp2.content.split()

        # Take first half from hyp1, second from hyp2
        mid1 = len(content1) // 2
        mid2 = len(content2) // 2

        merged_content = ' '.join(content1[:mid1] + content2[mid2:])

        merged = copy.deepcopy(hyp1)
        merged.content = merged_content
        merged.id = f"{hyp1.id}_{hyp2.id}_merge"
        merged.metadata = {
            'operation': 'merge',
            'parents': [hyp1.id, hyp2.id]
        }

        return merged

    def prune(self, hypotheses: List, scores: List[HypothesisScore],
              keep_ratio: float = 0.5) -> List:
        """
        Prune low-scoring hypotheses.

        Args:
            hypotheses: List of hypothesis objects
            scores: Corresponding scores
            keep_ratio: Fraction to keep (0-1)

        Returns:
            Pruned list of hypotheses
        """
        # Sort by score descending
        scored_pairs = sorted(zip(hypotheses, scores),
                            key=lambda x: x[1].score, reverse=True)

        keep_count = max(1, int(len(scored_pairs) * keep_ratio))
        pruned = [pair[0] for pair in scored_pairs[:keep_count]]

        return pruned

    def evolve(self, hypotheses: List, scores: List[HypothesisScore],
               target_population: int = 5) -> List:
        """
        Perform one evolution cycle: mutate, merge, prune.

        Args:
            hypotheses: Current hypothesis population
            scores: Their scores
            target_population: Desired population size

        Returns:
            Evolved hypothesis population
        """
        if not hypotheses:
            return []

        # Select best for evolution
        best_idx = scores.index(max(scores, key=lambda s: s.score))
        best_hyp = hypotheses[best_idx]

        evolved = [best_hyp]  # Keep the best

        # Generate mutations
        for _ in range(target_population // 3):
            mutated = self.mutate(best_hyp)
            evolved.append(mutated)

        # Generate merges if we have multiple hypotheses
        if len(hypotheses) > 1:
            for _ in range(target_population // 3):
                h1 = random.choice(hypotheses)
                h2 = random.choice([h for h in hypotheses if h != h1])
                merged = self.merge(h1, h2)
                evolved.append(merged)

        # Fill with random selections if needed
        while len(evolved) < target_population:
            evolved.append(random.choice(hypotheses))

        # Prune to target size
        if len(evolved) > target_population:
            # Simple pruning - keep first N
            evolved = evolved[:target_population]

        return evolved

    def should_accept_evolution(self, original_score: float, evolved_score: float,
                              novelty_score: float = 0.0) -> bool:
        """
        Determine if evolved hypothesis should be accepted.

        Args:
            original_score: Score of original hypothesis
            evolved_score: Score of evolved hypothesis
            novelty_score: Novelty measure (0-1)

        Returns:
            Whether to accept the evolution
        """
        return evolved_score >= original_score or novelty_score > self.novelty_threshold


# Example usage
if __name__ == "__main__":
    from kairoseed import Kairoseed
    from gsbs import GSBS

    # Generate initial hypotheses
    generator = Kairoseed(3)
    hyps = generator.generate_hypotheses("improve productivity")

    # Score them
    scorer = GSBS()
    scores = scorer.score_hypotheses(hyps)

    print("Original hypotheses:")
    for h, s in zip(hyps, scores):
        print(f"{h.id}: {h.content} -> {s.score:.3f}")

    # Evolve
    evolver = PEE()
    evolved = evolver.evolve(hyps, scores, target_population=4)

    print("\nEvolved hypotheses:")
    for h in evolved:
        print(f"{h.id}: {h.content}")