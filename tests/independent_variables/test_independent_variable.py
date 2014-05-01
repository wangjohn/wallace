from unittest import TestCase

from wallace.independent_variables import IndependentVariableSelection
from wallace.settings import AbstractSettings
from wallace.dataset import Dataset, DatasetVariable

class IndependentVariableSelectionTest(TestCase):

    def setUp(self):
        data_matrix = [[1,2,3], [2,3,4], [5,6,7]]
        headers = ["column_0", "column_1", "column_2"]
        self.header_dataset = Dataset(data_matrix, headers)
        self.nonheader_dataset = Dataset(data_matrix)

        self.headered_dependent_variable = DatasetVariable("column_0")
        self.nonheadered_dependent_variable = DatasetVariable(0)

    def test_initializing_small_dataset_with_header(self):
        settings = AbstractSettings()
        selection = IndependentVariableSelection(settings, self.header_dataset, self.headered_dependent_variable)

        variables = selection.initialize_independent_variables(2)
        headers = [var.variable for var in variables]
        self.assertIn("column_1", headers)
        self.assertIn("column_2", headers)

    def test_initializaing_small_dataset_without_header(self):
        settings = AbstractSettings()
        selection = IndependentVariableSelection(settings, self.nonheader_dataset, self.nonheadered_dependent_variable)

        variables = selection.initialize_independent_variables(2)
        headers = [var.variable for var in variables]
        self.assertIn(1, headers)
        self.assertIn(2, headers)

    def test_getting_probability_of_variables(self):
        settings = AbstractSettings()
        selection = IndependentVariableSelection(settings, self.header_dataset, self.headered_dependent_variable)

        self.assertAlmostEqual(0.5, selection.get_probability(DatasetVariable("column_1")))
        self.assertAlmostEqual(0.5, selection.get_probability(DatasetVariable("column_2")))

        self.assertAlmostEqual(0.5, selection.get_probability("column_1"))
        self.assertAlmostEqual(0.5, selection.get_probability("column_2"))

    def test_increasing_probability_of_variables(self):
        settings = AbstractSettings()
        selection = IndependentVariableSelection(settings, self.header_dataset, self.headered_dependent_variable)
        selection.increase_probability(DatasetVariable("column_1"))

        self.assertLess(0.5, selection.get_probability(DatasetVariable("column_1")))
        self.assertGreater(0.5, selection.get_probability(DatasetVariable("column_2")))
