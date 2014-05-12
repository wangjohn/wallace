from unittest import TestCase

from wallace.dataset_transformations.dataset_transformation import DatasetTransformation
from wallace.dataset_transformations.dataset_transformer import DatasetTransformer
from wallace.dataset import Dataset
from wallace.settings import AbstractSettings

class IdentityTransformation(DatasetTransformation):
    def transform_column(self, column):
        return column

class DatasetTransformerTest(TestCase):
    def setUp(self):
        self.settings = AbstractSettings()

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
        self.assertEqual([1,2,"hi",1,2,"hi"], result_matrix[0])
        self.assertEqual([2,3,"bye",2,3,"bye"], result_matrix[1])
        self.assertEqual(None, result.headers)

