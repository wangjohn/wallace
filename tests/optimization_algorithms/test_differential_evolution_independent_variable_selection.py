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
            "differential_evolution.crossover_probability": 1.0,
            "differential_evolution.differential_weight": 1.0,
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

        self.assertGreater(len(variables), 0)
        for var in variables:
            self.assertIsInstance(var, DatasetVariable)

    def test_getting_original_probability_from_model(self):
        for i in xrange(len(self.potential_independent_variables)):
            probability = self.de_variable_selection.original_probability(self.potential_independent_variables[i])
            self.assertAlmostEqual(float(1)/len(self.potential_independent_variables), probability)

    def test_getting_variable_probability_from_model(self):
        independent_variable_selections = [wrapper.independent_variable_selection for wrapper in self.model_population]

        probability = self.de_variable_selection.get_variable_probability(independent_variable_selections[:3], self.potential_independent_variables[0])
        self.assertAlmostEqual(float(1)/len(self.potential_independent_variables), probability)
