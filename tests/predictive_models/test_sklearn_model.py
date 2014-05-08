from unittest import TestCase

from wallace.predictive_models.sklearn_model import SklearnModel, TrainedSklearnModel
from wallace.dataset import Dataset, DatasetVariable
from wallace.parameters import ParameterSet
from wallace.settings import AbstractSettings

class SklearnModelTest(TestCase):
    def setUp(self):
        data_matrix = [
                [1,2,3,"a"],
                [2,3,2,"b"],
                [3,2,1,"a"],
                [5,5,1,"c"],
                [2,2,2,"a"]]
        self.dataset = Dataset(data_matrix)
        self.settings = AbstractSettings({})
        self.parameter_set = ParameterSet({})
        self.dependent_variable = DatasetVariable(0)
        self.independent_variables = [DatasetVariable(1), DatasetVariable(2), DatasetVariable(3)]

        self.sklearn_model = SklearnModel(self.settings, self.parameter_set, self.dependent_variable, self.independent_variables)

    def test_categorical_independent_variables(self):
        independent_variable_data = self.sklearn_model.get_independent_variable_data(self.dataset)

        self.assertEqual(5, len(independent_variable_data))
        num_categories = len(independent_variable_data[0])
        self.assertEqual(5, num_categories)

    def test_dependent_variable_data(self):
        dependent_variable_data = self.sklearn_model.get_dependent_variable_data(self.dataset)

        self.assertEqual(5, len(dependent_variable_data))
        self.assertListEqual([1,2,3,5,2], dependent_variable_data)
