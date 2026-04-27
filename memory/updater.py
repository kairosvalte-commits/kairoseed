"""
Weight Updater: Logic for updating scoring weights based on outcomes.
"""

from typing import Dict, List, Any, Tuple
import numpy as np


class WeightUpdater:
    """
    Handles weight updates for the GSBS scoring system.

    Implements various update strategies for adaptive learning.
    """

    def __init__(self, learning_rate: float = 0.1, adaptation_strategy: str = "error_based"):
        self.learning_rate = learning_rate
        self.adaptation_strategy = adaptation_strategy  # error_based, reinforcement, gradient

    def update_weights_error_based(self, current_weights: Dict[str, float],
                                 predicted_score: float, actual_outcome: float) -> Dict[str, float]:
        """
        Update weights based on prediction error.

        W_{t+1} = W_t + α (R_actual - R_predicted)
        """
        error = actual_outcome - predicted_score

        new_weights = {}
        for key, weight in current_weights.items():
            # Simple error-based update
            adjustment = self.learning_rate * error
            new_weights[key] = max(0.0, min(1.0, weight + adjustment))

        # Normalize to ensure weights sum appropriately
        total = sum(new_weights.values())
        if total > 0:
            new_weights = {k: v/total for k, v in new_weights.items()}

        return new_weights

    def update_weights_reinforcement(self, current_weights: Dict[str, float],
                                   action_taken: str, reward: float) -> Dict[str, float]:
        """
        Update weights using reinforcement learning principles.

        Args:
            current_weights: Current weight values
            action_taken: Which component was emphasized in decision
            reward: Reward signal (positive for good outcomes)
        """
        # Map actions to weight adjustments
        action_weights = {
            'success': {'success': 0.1, 'stability': -0.05, 'cost': -0.05, 'risk': 0.0},
            'stability': {'success': -0.05, 'stability': 0.1, 'cost': 0.0, 'risk': -0.05},
            'cost': {'success': 0.0, 'stability': -0.05, 'cost': 0.1, 'risk': -0.05},
            'risk': {'success': -0.05, 'stability': 0.0, 'cost': -0.05, 'risk': 0.1}
        }

        adjustments = action_weights.get(action_taken, {})

        new_weights = {}
        for key, weight in current_weights.items():
            adjustment = adjustments.get(key, 0.0) * reward * self.learning_rate
            new_weights[key] = max(0.0, min(1.0, weight + adjustment))

        return new_weights

    def update_weights_gradient(self, current_weights: Dict[str, float],
                              gradients: Dict[str, float]) -> Dict[str, float]:
        """
        Update weights using gradient descent.

        Args:
            current_weights: Current weights
            gradients: Gradient for each weight component
        """
        new_weights = {}
        for key, weight in current_weights.items():
            gradient = gradients.get(key, 0.0)
            new_weights[key] = max(0.0, min(1.0, weight - self.learning_rate * gradient))

        return new_weights

    def update(self, current_weights: Dict[str, float], **kwargs) -> Tuple[Dict[str, float], Dict[str, Any]]:
        """
        Main update method - dispatches to appropriate strategy.

        Returns:
            (new_weights, update_metadata)
        """
        if self.adaptation_strategy == "error_based":
            predicted = kwargs.get('predicted_score', 0.0)
            actual = kwargs.get('actual_outcome', 0.0)
            new_weights = self.update_weights_error_based(current_weights, predicted, actual)
            metadata = {'error': actual - predicted}

        elif self.adaptation_strategy == "reinforcement":
            action = kwargs.get('action_taken', '')
            reward = kwargs.get('reward', 0.0)
            new_weights = self.update_weights_reinforcement(current_weights, action, reward)
            metadata = {'action': action, 'reward': reward}

        elif self.adaptation_strategy == "gradient":
            gradients = kwargs.get('gradients', {})
            new_weights = self.update_weights_gradient(current_weights, gradients)
            metadata = {'gradients': gradients}

        else:
            # Default to error-based
            new_weights = current_weights.copy()
            metadata = {'strategy': 'unknown'}

        return new_weights, metadata

    def get_optimal_weights(self, decision_history: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Analyze decision history to find optimal weights.

        Args:
            decision_history: List of past decisions with outcomes

        Returns:
            Optimized weights
        """
        # Simple optimization: weight by success rate
        if not decision_history:
            return {'success': 0.4, 'stability': 0.3, 'cost': 0.2, 'risk': 0.1}

        # Count successes for each emphasized component
        component_success = {'success': 0, 'stability': 0, 'cost': 0, 'risk': 0}
        component_total = {'success': 0, 'stability': 0, 'cost': 0, 'risk': 0}

        for decision in decision_history:
            emphasized = decision.get('emphasized_component', 'success')
            success = decision.get('outcome', 0) > 0.5  # Binary success

            component_total[emphasized] += 1
            if success:
                component_success[emphasized] += 1

        # Calculate success rates
        optimal_weights = {}
        for component in component_success:
            if component_total[component] > 0:
                rate = component_success[component] / component_total[component]
                optimal_weights[component] = rate
            else:
                optimal_weights[component] = 0.25  # Default

        # Normalize
        total = sum(optimal_weights.values())
        if total > 0:
            optimal_weights = {k: v/total for k, v in optimal_weights.items()}

        return optimal_weights