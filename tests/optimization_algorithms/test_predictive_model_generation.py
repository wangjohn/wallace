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

    def test_normalizing_weights_with_all_weights_defined(self):
        model_types = {
                "model1": { "weight": 10 },
                "model2": { "weight": 20 },
                "model3": { "weight": 30 }
            }

        model_generator = PredictiveModelGenerator({})
        normalized_weights = model_generator._normalize_weights(model_types)

        self.assertAlmostEqual(float(1)/6, normalized_weights["model1"])
        self.assertAlmostEqual(float(2)/6, normalized_weights["model2"])
        self.assertAlmostEqual(float(3)/6, normalized_weights["model3"])

    def test_normalizing_weights_with_some_weights_undefined(self):
        model_types = {
                "model1": { "weight": 5 },
                "model2": { "weight": None },
                "model3": { "weight": 15 },
                "model4": {}
            }

        model_generator = PredictiveModelGenerator({})
        normalized_weights = model_generator._normalize_weights(model_types)

        self.assertAlmostEqual(float(5)/40, normalized_weights["model1"])
        self.assertAlmostEqual(float(10)/40, normalized_weights["model2"])
        self.assertAlmostEqual(float(15)/40, normalized_weights["model3"])
        self.assertAlmostEqual(float(10)/40, normalized_weights["model4"])
