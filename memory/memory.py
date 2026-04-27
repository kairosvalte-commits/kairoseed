"""
Memory System: Weight storage and history logging for Kairoseed.
"""

from typing import Dict, List, Any, Optional
import json
import os
from datetime import datetime
from models.decision import Decision


class Memory:
    """
    Persistent memory system for Kairoseed.

    Stores decision history, weight evolution, and learning data.
    """

    def __init__(self, storage_path: str = "memory/store.json"):
        self.storage_path = storage_path
        self.weights_history: List[Dict[str, Any]] = []
        self.decision_history: List[Decision] = []
        self.current_weights: Dict[str, float] = {
            'success': 0.4,
            'stability': 0.3,
            'cost': 0.2,
            'risk': 0.1
        }
        self.learning_rate: float = 0.1

        # Load existing memory if available
        self.load()

    def store_decision(self, decision: Decision):
        """Store a decision in memory."""
        self.decision_history.append(decision)
        self.save()

    def update_weights(self, predicted_score: float, actual_outcome: float):
        """
        Update weights based on prediction error.

        W_{t+1} = W_t + α (R_actual - R_predicted)
        """
        error = actual_outcome - predicted_score

        # Update weights proportionally to error
        for key in self.current_weights:
            adjustment = self.learning_rate * error
            self.current_weights[key] = max(0.0, min(1.0,
                self.current_weights[key] + adjustment))

        # Normalize weights to sum to 1
        total = sum(self.current_weights.values())
        if total > 0:
            self.current_weights = {k: v/total for k, v in self.current_weights.items()}

        # Store weight snapshot
        self.weights_history.append({
            'timestamp': datetime.now().isoformat(),
            'weights': self.current_weights.copy(),
            'error': error,
            'predicted': predicted_score,
            'actual': actual_outcome
        })

        self.save()

    def get_weights(self) -> Dict[str, float]:
        """Get current weights."""
        return self.current_weights.copy()

    def get_recent_history(self, limit: int = 10) -> List[Decision]:
        """Get recent decision history."""
        return self.decision_history[-limit:] if self.decision_history else []

    def get_weight_evolution(self) -> List[Dict[str, Any]]:
        """Get weight evolution history."""
        return self.weights_history.copy()

    def save(self):
        """Save memory to disk."""
        data = {
            'current_weights': self.current_weights,
            'weights_history': self.weights_history,
            'decision_history': [d.to_dict() for d in self.decision_history],
            'learning_rate': self.learning_rate
        }

        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self):
        """Load memory from disk."""
        if not os.path.exists(self.storage_path):
            return

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            self.current_weights = data.get('current_weights', self.current_weights)
            self.weights_history = data.get('weights_history', [])
            self.learning_rate = data.get('learning_rate', self.learning_rate)

            # Reconstruct decisions
            decision_dicts = data.get('decision_history', [])
            self.decision_history = [Decision.from_dict(d) for d in decision_dicts]

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not load memory: {e}")

    def clear(self):
        """Clear all memory."""
        self.weights_history = []
        self.decision_history = []
        self.current_weights = {
            'success': 0.4,
            'stability': 0.3,
            'cost': 0.2,
            'risk': 0.1
        }
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)