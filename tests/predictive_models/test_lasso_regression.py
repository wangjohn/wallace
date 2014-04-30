from unittest import TestCase

from wallace.predictive_models.lasso_regression import LassoRegression
from wallace.dataset import Dataset, DatasetVariable
from wallace.parameters import ParameterSet

class RidgeRegressionTest(TestCase):
    def setUp(self):
        dictionary = {
            "lasso_regression_alpha": {
                "type": "range",
                "lower_bound": 0.3,
                "upper_bound": 0.9,
                "default": 0.5
                }
            }
        self.parameter_set = ParameterSet.create_from_dict(dictionary)

    def test_training_ridge_on_simple_dataset(self):
        settings = {}
        dependent_variable = DatasetVariable(0)
        independent_variables = [DatasetVariable(1)]
        regression = LassoRegression(settings, self.parameter_set, dependent_variable, independent_variables)

        data_matrix = [[1,1], [2,2], [3,3], [4,4]]
        dataset = Dataset(data_matrix)

        trained = regression.train(dataset)
        array = trained.predict(dataset)

        self.assertAlmostEqual(1.6, array[0])
        self.assertAlmostEqual(2.2, array[1])
        self.assertAlmostEqual(2.8, array[2])
        self.assertAlmostEqual(3.4, array[3])
