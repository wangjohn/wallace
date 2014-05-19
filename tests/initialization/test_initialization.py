from unittest import TestCase

from wallace.settings import AbstractSettings
from wallace.initialization import WallaceInitialization

from wallace.predictive_models.lasso_regression import LassoRegression
from wallace.predictive_models.ols_linear_regression import OLSLinearRegression
from wallace.predictive_models.random_forest_regression import RandomForestRegression
from wallace.predictive_models.ridge_regression import RidgeRegression

class InitializationTest(TestCase):
    def setUp(self):
        self.settings = AbstractSettings()

    def test_creating_predictive_model_generator(self):
        models = {
            LassoRegression: None,
            OLSLinearRegression: None,
            RandomForestRegression: None,
            RidgeRegression: None
            }
        generator = WallaceInitialization(self.settings).create_predictive_model_generator(models)
        self.assertEqual(4, len(generator.list_model_types()))

        for model_information in generator.list_model_types():
            self.assertEqual(2, len(model_information))
            self.assertIn("model_class", model_information)
            self.assertIn("parameter_validity_check", model_information)

    def test_read_filename(self):
        pass
