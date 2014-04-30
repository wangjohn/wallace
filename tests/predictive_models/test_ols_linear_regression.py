from unittest import TestCase

from wallace.predictive_models.ols_linear_regression import OLSLinearRegression
from wallace.dataset import Dataset, DatasetVariable

class OLSRegressionTest(TestCase):
    def test_training_ols_on_simple_dataset(self):
        settings = {}
        parameter_set = {}
        dependent_variable = DatasetVariable(0)
        independent_variables = [DatasetVariable(1)]
        regression = OLSLinearRegression(settings, parameter_set, dependent_variable, independent_variables)

        data_matrix = [[1,1], [2,2], [3,3], [4,4]]
        dataset = Dataset(data_matrix)

        trained = regression.train(dataset)
        array = trained.predict(dataset)

        self.assertEqual(1, array[0])
        self.assertEqual(2, array[1])
        self.assertEqual(3, array[2])
        self.assertEqual(4, array[3])

    def test_training_ols_on_simple_dataset_two_variables(self):
        settings = {}
        parameter_set = {}
        dependent_variable = DatasetVariable(0)
        independent_variables = [DatasetVariable(1), DatasetVariable(2)]
        regression = OLSLinearRegression(settings, parameter_set, dependent_variable, independent_variables)

        data_matrix = [[1,1,2], [2,2,3], [3,3,4], [4,4,5]]
        dataset = Dataset(data_matrix)

        trained = regression.train(dataset)
        array = trained.predict(dataset)

        self.assertAlmostEqual(1, array[0])
        self.assertAlmostEqual(2, array[1])
        self.assertAlmostEqual(3, array[2])
        self.assertAlmostEqual(4, array[3])
