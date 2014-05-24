from unittest import TestCase

from wallace.optimization_algorithms.optimization_algorithm_stage_handler import OptimizationAlgorithmStageHandler
from wallace.optimization_algorithms.stage.optimization_algorithm_stage import OptimizationAlgorithmStage
from wallace.settings import AbstractSettings

class FakeException(Exception):
    def __init__(self, value):
        self.value = value

class FakeStage1(OptimizationAlgorithmStage):
    def before_stage(self):
        raise FakeException("before_stage.fake_stage1")

    def after_stage(self):
        raise FakeException("after_stage.fake_stage1")

    def on_step(self):
        raise FakeException("on_step.fake_stage1")

class FakeStage2(OptimizationAlgorithmStage):
    def before_stage(self):
        raise FakeException("before_stage.fake_stage2")

    def after_stage(self):
        raise FakeException("after_stage.fake_stage2")

    def on_step(self):
        raise FakeException("on_step.fake_stage2")

class OptimizationAlgorithmStageHandlerTest(TestCase):
    def setUp(self):
        self.settings = AbstractSettings()

    def test_stage_handler_for_simple_stage_progression(self):
        stage_handler = OptimizationAlgorithmStageHandler(self.settings, {
                FakeStage1: (0.0, 0.5),
                FakeStage2: (0.5, 1.0)
            })

        with self.assertRaises(FakeException) as fake_stage1_exception:
            stage_handler.run_stage(0, total_steps=2)

        with self.assertRaises(FakeException) as fake_stage2_exception:
            stage_handler.run_stage(1, total_steps=2)

        self.assertEqual("before_stage.fake_stage1", fake_stage1_exception.exception.value)
        self.assertEqual("before_stage.fake_stage2", fake_stage2_exception.exception.value)
