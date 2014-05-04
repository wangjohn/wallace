from unittest import TestCase

from wallace.optimization_algorithms.differential_evolution import DEIndependentVariableSelection
from wallace.optimization_algorithms.optimization_algorithm import OptimizationAlgorithmModelWrapper
from wallace.settings import AbstractSettings
from wallace.dataset import DatasetVariable
from wallace.independent_variables import IndependentVariableSelection
from wallace.predictive_models.predictive_model import PredictiveModel
from wallace.parameters import ParameterSet

class DEIndependentVariableSelectionTest(TestCase):
    def setUp(self):
        dependent_variable = DatasetVariable(0)
        independent_variables = [DatasetVariable(1), DatasetVariable(2), DatasetVariable(3)]
        settings = AbstractSettings({
            "differential_evolution.crossover_probability": 0.5,
            "differential_evolution.differential_weight": 0.8,
            "independent_variable_selection.initial_independent_variables_percentage": 0.25
            })

        model_population = []
        for i in xrange(4):
            model = PredictiveModel(settings, ParameterSet({}), dependent_variable, independent_variables)
            independent_variable_selection = IndependentVariableSelection(settings, dependent_variable, independent_variables)
            model_population.append(OptimizationAlgorithmModelWrapper(model, independent_variable_selection))
        self.model_population = model_population
        self.settings = settings
        self.potential_independent_variables = independent_variables
        self.target_wrapper = model_population[0]

        self.de_variable_selection = DEIndependentVariableSelection(self.settings, self.target_wrapper, self.model_population, self.potential_independent_variables)

    def test_generate_independent_variables(self):
        variables = self.de_variable_selection.generate_independent_variables()

        self.assertEqual(3, len(variables))
        for var in variables:
            self.assertIsInstance(var, DatasetVariable)

