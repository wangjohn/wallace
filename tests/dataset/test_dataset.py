from unittest import TestCase

from wallace.dataset import Dataset, DatasetVariable

class DatasetTest(TestCase):
    def setUp(self):
        data_matrix = [
                [0,"detective", "book"],
                [1, "pablo", "escobar"],
                [2, "african", "queen"],
                [3, "applause", "movie"]
                ]
        headers = ["number", "string", "another_string"]
        self.dataset = Dataset(data_matrix, headers)

    def test_getting_independent_variables(self):
        dependent_variable_index = DatasetVariable(0)
        dependent_variable_header = DatasetVariable("number")

        independent_variables = self.dataset.get_independent_variables(dependent_variable_index)
        self.assertEqual(2, len(independent_variables))
        for variable in independent_variables:
            self.assertIn(variable.variable, ["string", "another_string"])

        independent_variables = self.dataset.get_independent_variables(dependent_variable_header)
        self.assertEqual(2, len(independent_variables))
        for variable in independent_variables:
            self.assertIn(variable.variable, ["string", "another_string"])

    def test_crossfold_partitions(self):
        past_test_datasets = []
        for training_dataset, test_dataset in self.dataset.crossfold_partitions(4):
            self.assertEqual(3, training_dataset.num_rows)
            self.assertEqual(1, test_dataset.num_rows)
            self.assertNotIn(test_dataset.get(0, 0), past_test_datasets)

            past_test_datasets.append(test_dataset.get(0, 0))

    def test_get_filtered_matrix(self):
        variables = [DatasetVariable(0), DatasetVariable("string")]

        filtered_matrix = self.dataset.get_filtered_matrix(variables)
        self.assertEqual(4, len(filtered_matrix))
        for i in xrange(len(filtered_matrix)):
            self.assertEqual(2, len(filtered_matrix[i]))

        self.assertListEqual([0, "detective"], filtered_matrix[0])
        self.assertListEqual([1, "pablo"], filtered_matrix[1])
        self.assertListEqual([2, "african"], filtered_matrix[2])
        self.assertListEqual([3, "applause"], filtered_matrix[3])

    def test_getting_filtered_matrix_with_no_variables(self):
        variables = []

        with self.assertRaises(ValueError):
            filtered_matrix = self.dataset.get_filtered_matrix(variables)
