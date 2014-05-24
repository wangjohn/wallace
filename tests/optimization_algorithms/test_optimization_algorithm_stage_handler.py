from unittest import TestCase

from wallace.optimization_algorithms.optimization_algorithm_stage_handler import OptimizationAlgorithmStageHandler
from wallace.optimization_algorithms.stage.optimization_algorithm_stage import OptimizationAlgorithmStage
from wallace.settings import AbstractSettings

class FakeStage1(OptimizationAlgorithmStage):
    def before_stage(self, payload):
        payload.append("before_stage.fake_stage1")

    def after_stage(self, payload):
        payload.append("after_stage.fake_stage1")

    def on_step(self, payload):
        payload.append("on_step.fake_stage1")

class FakeStage2(OptimizationAlgorithmStage):
    def before_stage(self, payload):
        payload.append("before_stage.fake_stage2")

    def after_stage(self, payload):
        payload.append("after_stage.fake_stage2")

class FakeStage3(OptimizationAlgorithmStage):
    def on_step(self, payload):
        payload.append("on_step.fake_stage3")

class OptimizationAlgorithmStageHandlerTest(TestCase):
    def setUp(self):
        self.settings = AbstractSettings()

    def test_stage_handler_for_simple_stage_progression(self):
        stage_handler = OptimizationAlgorithmStageHandler(self.settings, {
                FakeStage1: (0.0, 0.5),
                FakeStage2: (0.5, 1.0)
            })

        payload = []
        stage_handler.run_stage(0, total_steps=2, payload=payload)
        stage_handler.run_stage(1, total_steps=2, payload=payload)

        self.assertEqual(5, len(payload))
        self.assertEqual("before_stage.fake_stage1", payload[0])
        self.assertEqual("on_step.fake_stage1", payload[1])
        self.assertEqual("after_stage.fake_stage1", payload[2])
        self.assertEqual("before_stage.fake_stage2", payload[3])
        self.assertEqual("after_stage.fake_stage2", payload[4])

    def test_stage_handler_for_multi_step_stage_progression_with_holes(self):
        stage_handler = OptimizationAlgorithmStageHandler(self.settings, {
                FakeStage1: (0.1, 0.3),
                FakeStage2: (0.4, 0.5),
                FakeStage3: (0.5, 0.6)
            })

        payload = []
        for i in xrange(10):
            stage_handler.run_stage(i, total_steps=10, payload=payload)

        self.assertEqual(9, len(payload))
        self.assertEqual("before_stage.fake_stage1", payload[0])
        self.assertEqual("on_step.fake_stage1", payload[1])
        self.assertEqual("after_stage.fake_stage1", payload[2])
        self.assertEqual("before_stage.fake_stage1", payload[3])
        self.assertEqual("on_step.fake_stage1", payload[4])
        self.assertEqual("after_stage.fake_stage1", payload[5])
        self.assertEqual("before_stage.fake_stage2", payload[6])
        self.assertEqual("after_stage.fake_stage2", payload[7])
        self.assertEqual("on_step.fake_stage3", payload[8])
