from unittest import TestCase

from wallace.categorical_variable_encoder import CategoricalVariableEncoder

class CategoricalVariableEncoderTest(TestCase):
    def setUp(self):
        self.data_matrix = [
                ["1","2","a","b"],
                ["2","2","c","d"],
                ["1","2","c","f"],
                ["1","2","d","g"],
                ["5","3","d","m"]
                ]
        self.categorical_indices = [2,3]
        self.categorical_variable_encoder = CategoricalVariableEncoder()

    def test_getting_category_values(self):
        category_values = self.categorical_variable_encoder.get_category_values(self.data_matrix, self.categorical_indices)

        self.assertEqual(3, len(category_values[2]))
        self.assertIn("a", category_values[2])
        self.assertIn("c", category_values[2])
        self.assertIn("d", category_values[2])

        self.assertEqual(5, len(category_values[3]))
        self.assertIn("b", category_values[3])
        self.assertIn("d", category_values[3])
        self.assertIn("f", category_values[3])
        self.assertIn("g", category_values[3])
        self.assertIn("m", category_values[3])

    def test_getting_category_mapping(self):
        category_mapping = self.categorical_variable_encoder.get_category_value_mapping(self.data_matrix, self.categorical_indices)

        self.assertEqual(3, len(category_mapping[2]))
        self.assertEqual(0, category_mapping[2]["a"])
        self.assertEqual(1, category_mapping[2]["c"])
        self.assertEqual(2, category_mapping[2]["d"])

        self.assertEqual(5, len(category_mapping[3]))
        self.assertEqual(0, category_mapping[3]["b"])
        self.assertEqual(1, category_mapping[3]["d"])
        self.assertEqual(2, category_mapping[3]["f"])
        self.assertEqual(3, category_mapping[3]["g"])
        self.assertEqual(4, category_mapping[3]["m"])

    def test_converting_categorical_variables(self):
        data_matrix = self.categorical_variable_encoder.convert_categorical_variables(self.data_matrix, self.categorical_indices)

        self.assertEqual(5, len(data_matrix))
        self.assertListEqual(["1","2",0,0], data_matrix[0])
        self.assertListEqual(["1","2",1,1], data_matrix[1])
        self.assertListEqual(["1","2",1,2], data_matrix[0])
        self.assertListEqual(["1","2",2,3], data_matrix[0])
        self.assertListEqual(["1","2",2,4], data_matrix[0])

