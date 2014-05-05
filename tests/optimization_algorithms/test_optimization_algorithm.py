from unittest import TestCase

from wallace.optimization_algorithms.optimization_algorithm import OptimizationAlgorithm, OptimizationAlgorithmModelWrapper
from wallace.optimization_algorithms.predictive_model_generator import PredictiveModelGenerator
from wallace.dataset import Dataset, DatasetVariable
from wallace.predictive_models.predictive_model import PredictiveModel
from wallace.settings import AbstractSettings
from wallace.parameters import ParametersGeneralValidityCheck
from wallace.independent_variables import IndependentVariableSelection

class FakePredictiveModel(PredictiveModel):
    @classmethod
    def validity_check(klass):
        validity_check = ParametersGeneralValidityCheck()
        validity_check.set_range_parameter("range_param_0", 0.0, 1.0)
        validity_check.set_range_parameter("range_param_1", 0.0, 1.0)
        validity_check.set_range_parameter("range_param_2", 0.0, 1.0)
        validity_check.set_category_parameter("category_param_0", ["0","1","2","3"])
        validity_check.set_category_parameter("category_param_1", ["0","1","2","3"], [0.1, 0.1, 0.3, 0.5])
        return validity_check

class OptimizationAlgorithmTest(TestCase):
    def setUp(self):
        data_matrix = [[1,2,3,4], [2,3,4,5], [3,4,5,6], [0,1,3,4]]
        dataset = Dataset(data_matrix)
        dependent_variable = DatasetVariable(0)
        settings = AbstractSettings({
            "differential_evolution.crossover_probability": 1.0,
            "differential_evolution.differential_weight": 1.0,
            "optimization_algorithm.population_size": 5,
            "independent_variable_selection.initial_independent_variables_percentage": 1.0
            })

        predictive_model_generator = PredictiveModelGenerator(settings)
        predictive_model_generator.add_model_type(FakePredictiveModel)

        self.optimization_algorithm = OptimizationAlgorithm(dataset, dependent_variable, settings, predictive_model_generator)

    def assert_in_range(self, value, lower_bound, upper_bound):
        self.assertGreaterEqual(value, lower_bound)
        self.assertLessEqual(value, upper_bound)

    def test_initialization_of_optimization_algorithm(self):
        self.optimization_algorithm.initialize_population()
        self.assertEqual(5, len(self.optimization_algorithm.model_population))

        for model_wrapper in self.optimization_algorithm.model_population:
            self.assertIsInstance(model_wrapper, OptimizationAlgorithmModelWrapper)
            self.assertIsInstance(model_wrapper.model, FakePredictiveModel)
            self.assertIsInstance(model_wrapper.independent_variable_selection, IndependentVariableSelection)

            self.assertEqual(3, len(model_wrapper.model.independent_variables))
            self.assert_in_range(model_wrapper.model.parameter_set.get("range_param_0"), 0.0, 1.0)
            self.assert_in_range(model_wrapper.model.parameter_set.get("range_param_1"), 0.0, 1.0)
            self.assert_in_range(model_wrapper.model.parameter_set.get("range_param_2"), 0.0, 1.0)
            self.assertIn(model_wrapper.model.parameter_set.get("category_param_0"), ["0", "1", "2", "3"])
            self.assertIn(model_wrapper.model.parameter_set.get("category_param_1"), ["0", "1", "2", "3"])
