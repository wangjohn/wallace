from unittest import TestCase

from wallace.dataset_transformations.dataset_transformation import DatasetTransformation
from wallace.dataset_transformations.dataset_transformer import DatasetTransformer
from wallace.dataset import Dataset
from wallace.settings import AbstractSettings

class IdentityTransformation(DatasetTransformation):
    def transform_column(self, column):
        return column

    def valid_data_types(self):
        return ["integer", "float", "string"]

class DatasetTransformerTest(TestCase):
    def setUp(self):
        self.settings = AbstractSettings()
        self.transformations = [IdentityTransformation]
        self.transformer = DatasetTransformer(self.settings, self.transformations)

    def test_using_transformer_on_single_transformation(self):
        data_matrix = [
                [1,2,"hi"],
                [2,3,"bye"]
                ]
        dataset = Dataset(data_matrix)
        transformations = [IdentityTransformation]
        transformer = DatasetTransformer(self.settings, transformations)

        result = transformer.transform(dataset)
        result_matrix = result.data_matrix

        self.assertEqual(2, result.num_rows)
        self.assertEqual(6, result.num_cols)
        self.assertListEqual([1,2,"hi",1,2,"hi"], result_matrix[0])
        self.assertListEqual([2,3,"bye",2,3,"bye"], result_matrix[1])
        self.assertEqual(None, result.headers)

    def test_using_transformer_on_multiple_transformations(self):
        data_matrix = [
                [1,2,"hi"],
                [2,3,"bye"]
                ]
        dataset = Dataset(data_matrix)
        transformations = [IdentityTransformation, IdentityTransformation]
        transformer = DatasetTransformer(self.settings, transformations)

        result = transformer.transform(dataset)
        result_matrix = result.data_matrix

        self.assertEqual(2, result.num_rows)
        self.assertEqual(9, result.num_cols)
        self.assertListEqual([1,2,"hi",1,2,"hi",1,2,"hi"], result_matrix[0])
        self.assertListEqual([2,3,"bye",2,3,"bye",2,3,"bye"], result_matrix[1])
        self.assertEqual(None, result.headers)

    def test_using_transformer_on_data_matrix_with_headers(self):
        data_matrix = [
                [1,2,"hi"],
                [2,3,"bye"]
                ]
        dataset = Dataset(data_matrix, ["h0", "h1", "h2"])
        transformations = [IdentityTransformation]
        transformer = DatasetTransformer(self.settings, transformations)

        result = transformer.transform(dataset)
        result_matrix = result.data_matrix

        self.assertEqual(2, result.num_rows)
        self.assertEqual(6, result.num_cols)
        self.assertListEqual([1,2,"hi",1,2,"hi"], result_matrix[0])
        self.assertListEqual([2,3,"bye",2,3,"bye"], result_matrix[1])
        self.assertEqual(6, len(result.headers))
        self.assertListEqual(["h0", "h1", "h2", "identitytransformation_h0", "identitytransformation_h1", "identitytransformation_h2"], result.headers)

    def test_dataset_merging_without_headers(self):
        data_matrix_1 = [
                [1,2],
                [3,4]
                ]
        data_matrix_2 = [
                [5,6],
                [7,8]
                ]
        merged_dataset = self.transformer.merge_datasets([Dataset(data_matrix_1), Dataset(data_matrix_2)])

        self.assertEqual(2, merged_dataset.num_rows)
        self.assertEqual(4, merged_dataset.num_cols)
        self.assertListEqual([1,2,5,6], merged_dataset.data_matrix[0])
        self.assertListEqual([3,4,7,8], merged_dataset.data_matrix[1])
        self.assertEqual(None, merged_dataset.headers)

    def test_dataset_merging_with_headers(self):
        data_matrix_1 = [
                [1,2],
                [3,4]
                ]
        dataset_1 = Dataset(data_matrix_1, ["h0", "h1"])
        data_matrix_2 = [
                [5,6],
                [7,8]
                ]
        dataset_2 = Dataset(data_matrix_2, ["h2", "h3"])
        merged_dataset = self.transformer.merge_datasets([dataset_1, dataset_2])

        self.assertEqual(2, merged_dataset.num_rows)
        self.assertEqual(4, merged_dataset.num_cols)
        self.assertListEqual([1,2,5,6], merged_dataset.data_matrix[0])
        self.assertListEqual([3,4,7,8], merged_dataset.data_matrix[1])
        self.assertListEqual(["h0", "h1", "h2", "h3"], merged_dataset.headers)

    def test_dataset_merging_with_different_number_of_rows(self):
        data_matrix_1 = [
                [1,2],
                [3,4],
                [10,11]
                ]
        dataset_1 = Dataset(data_matrix_1, ["h0", "h1"])
        data_matrix_2 = [
                [5,6],
                [7,8]
                ]
        dataset_2 = Dataset(data_matrix_2, ["h2", "h3"])
        with self.assertRaises(ValueError):
            merged_dataset = self.transformer.merge_datasets([dataset_1, dataset_2])

    def test_dataset_merging_with_different_types_of_headers(self):
        data_matrix_1 = [
                [1,2],
                [3,4]
                ]
        dataset_1 = Dataset(data_matrix_1, ["h0", "h1"])
        data_matrix_2 = [
                [5,6],
                [7,8]
                ]
        dataset_2 = Dataset(data_matrix_2, None)
        with self.assertRaises(ValueError):
            merged_dataset = self.transformer.merge_datasets([dataset_1, dataset_2])
