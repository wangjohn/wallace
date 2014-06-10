from unittest import TestCase

from wallace.initialization import WallaceInitialization
from wallace.optimization_algorithms.differential_evolution import DifferentialEvolution
from wallace.predictive_models.ols_linear_regression import OLSLinearRegression
from wallace.settings import AbstractSettings
from wallace.dataset import DatasetVariable

import os

class OptimizationAlgorithmInitializationStageTest(TestCase):

    def setUp(self):
        self.settings = AbstractSettings()
        self.initialization = WallaceInitialization(self.settings)

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), './sample_regression_data.csv'))
        self.dataset = self.initialization.read_filename(path)
        self.dependent_variable = DatasetVariable("X1")

    def test_initialization_stage_uses_ols_regression_only(self):
        predictive_model_generator = self.initialization.create_predictive_model_generator()
        differential_evolution = DifferentialEvolution(self.dataset, self.dependent_variable, self.settings, predictive_model_generator)

        differential_evolution.initialize_population()

        for i in xrange(10):
            differential_evolution.step()
            current_population = differential_evolution.model_population

            for wrapper in current_population:
                self.assertIsInstance(wrapper.model, OLSLinearRegression)

