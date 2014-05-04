from unittest import TestCase

from wallace.optimization_algorithms.optimization_algorithm import OptimizationAlgorithmModelWrapper
from wallace.optimization_algorithms.differential_evolution import DEParameterSelection
from wallace.settings import AbstractSettings
from wallace.predictive_models.predictive_model import PredictiveModel
from wallace.parameters import ParameterSet, ParametersGeneralValidityCheck
from wallace.dataset import DatasetVariable

class FakePredictiveModel(PredictiveModel):
    @classmethod
    def required_parameters(klass):
        return ["range_param_0", "range_param_1", "range_param_2", "category_param_0", "category_param_1"]

class DEParameterSelectionTest(TestCase):
    def setUp(self):
        dependent_variable = DatasetVariable(0)
        independent_variables = [DatasetVariable(1), DatasetVariable(2)]
        settings = AbstractSettings({
            "differential_evolution.crossover_probability": 1.0,
            "differential_evolution.differential_weight": 1.0,
            })
        validity_check = ParametersGeneralValidityCheck()
        validity_check.set_range_parameter("range_param_0", 0.0, 1.0)
        validity_check.set_range_parameter("range_param_1", 0.0, 1.0)
        validity_check.set_range_parameter("range_param_2", 0.0, 1.0)
        validity_check.set_category_parameter("category_param_0", ["0","1","2","3"])
        validity_check.set_category_parameter("category_param_1", ["0","1","2","3"], [0.1, 0.1, 0.3, 0.5])

        model_population = []
        for i in xrange(4):
            parameter_values = {
                    "range_param_0": 0.5,
                    "range_param_1": 0.5,
                    "range_param_2": 0.5,
                    "category_param_0": "0",
                    "category_param_1": "0"
                    }
            parameter_set = ParameterSet(parameter_values, validity_check)
            model = FakePredictiveModel(settings, parameter_set, dependent_variable, independent_variables)
            wrapper = OptimizationAlgorithmModelWrapper(model, "fake_independent_variable_selection")
            model_population.append(wrapper)

        self.model_population = model_population
        self.validity_check = validity_check
        self.settings = settings
        self.target_wrapper = model_population[0]
        self.de_parameter_selection = DEParameterSelection(settings, self.target_wrapper, model_population, validity_check)

    def test_generation_of_parameter_set(self):
        parameter_set = self.de_parameter_selection.generate_parameter_set()

        self.assertEqual(0.5, parameter_set.get("range_param_0"))
        self.assertEqual(0.5, parameter_set.get("range_param_1"))
        self.assertEqual(0.5, parameter_set.get("range_param_2"))
        self.assertEqual(0.5, parameter_set.get("category_param_0"))
        self.assertEqual(0.5, parameter_set.get("category_param_1"))

