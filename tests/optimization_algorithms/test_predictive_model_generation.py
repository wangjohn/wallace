from unittest import TestCase

from wallace.predictive_models.predictive_model import PredictiveModel
from wallace.optimization_algorithms.predictive_model_generator import PredictiveModelGenerator

class PredictiveModelGeneratorTests(TestCase):
    def test_choosing_model_type(self):
        model_generator = PredictiveModelGenerator({})
        model_generator.add_model_type(PredictiveModel, "fake_validity_check")

        chosen_model = model_generator.choose_model_type()
        self.assertEqual(PredictiveModel, chosen_model["model_class"])
        self.assertEqual("fake_validity_check", chosen_model["parameter_validity_check"])
        self.assertEqual(None, chosen_model["weight"])

    def test_default_validity_check(self):
        model_generator = PredictiveModelGenerator({}, "default_validity_check")
        model_generator.add_model_type(PredictiveModel)

        chosen_model = model_generator.choose_model_type()
        self.assertEqual(PredictiveModel, chosen_model["model_class"])
        self.assertEqual("default_validity_check", chosen_model["parameter_validity_check"])
        self.assertEqual(None, chosen_model["weight"])
