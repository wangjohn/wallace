from unittest import TestCase

from wallace.predictive_models.extra_trees_regression import ExtraTreesRegression
from wallace.dataset import Dataset, DatasetVariable
from wallace.parameters import ParameterSet
from wallace.settings import AbstractSettings

class ExtraTreesRegressionTest(TestCase):
    def setUp(self):
        validity_check = ExtraTreesRegression.validity_check()
        parameters = {}
        for parameter_name in validity_check.list_parameter_names():
            parameters[parameter_name] = validity_check.get_valid_value(parameter_name)

        self.parameter_set = ParameterSet(parameters, validity_check=validity_check)

    def test_training_decision_tree_on_simple_dataset(self):
        settings = AbstractSettings({})
        dependent_variable = DatasetVariable(0)
        independent_variables = [DatasetVariable(1)]
        regression = ExtraTreesRegression(settings, self.parameter_set, dependent_variable, independent_variables)

        data_matrix = [[1,1], [2,2], [3,3], [4,4]]
        dataset = Dataset(data_matrix)

        trained = regression.train(dataset)
        array = trained.predict(dataset)

        self.assertEqual(4, len(array))
