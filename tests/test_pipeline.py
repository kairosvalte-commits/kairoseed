"""
Tests for Kairoseed Pipeline.
"""

import unittest
from core.pipeline import KairoseedPipeline, PipelineResult


class TestPipeline(unittest.TestCase):
    """Test cases for the complete Kairoseed pipeline."""

    def setUp(self):
        """Set up test fixtures."""
        self.pipeline = KairoseedPipeline(num_hypotheses=3, evolution_iterations=1)

    def test_pipeline_run(self):
        """Test basic pipeline execution."""
        input_state = "test input"
        result = self.pipeline.run(input_state, use_evolution=False)

        self.assertIsInstance(result, PipelineResult)
        self.assertEqual(result.input_state, input_state)
        self.assertIsNotNone(result.selected_hypothesis)
        self.assertIsNotNone(result.decision)
        self.assertIsNotNone(result.result)

    def test_pipeline_with_evolution(self):
        """Test pipeline with evolution enabled."""
        input_state = "evolve this"
        result = self.pipeline.run(input_state, use_evolution=True)

        self.assertIsInstance(result, PipelineResult)
        self.assertEqual(result.input_state, input_state)

    def test_agt_integration(self):
        """Test pipeline with AGT safety gate."""
        def mock_agt(hyp):
            return True  # Always approve

        input_state = "safe action"
        result = self.pipeline.run_with_agt(input_state, mock_agt)

        self.assertIsInstance(result, PipelineResult)
        self.assertNotEqual(result.decision, "Blocked by AGT safety gate")

    def test_agt_blocking(self):
        """Test AGT blocking unsafe hypotheses."""
        def strict_agt(hyp):
            return False  # Always block

        input_state = "unsafe action"
        result = self.pipeline.run_with_agt(input_state, strict_agt)

        self.assertEqual(result.decision, "Blocked by AGT safety gate")

    def test_result_json(self):
        """Test JSON serialization of results."""
        result = self.pipeline.run("test", use_evolution=False)
        json_str = result.to_json()

        self.assertIsInstance(json_str, str)
        self.assertIn("input", json_str)
        self.assertIn("selected", json_str)
        self.assertIn("decision", json_str)

    def test_empty_input(self):
        """Test pipeline with empty input."""
        result = self.pipeline.run("", use_evolution=False)

        self.assertIsInstance(result, PipelineResult)
        self.assertEqual(result.input_state, "")


if __name__ == '__main__':
    unittest.main()