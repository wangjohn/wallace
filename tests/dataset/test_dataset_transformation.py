from unittest import TestCase

from wallace.settings import AbstractSettings
from wallace.dataset_transformations.dataset_transformation import DatasetTransformation
from wallace.dataset import Dataset, DatasetVariable

class IdentityTransformation(DatasetTransformation):
    def transform_column(self, column):
        return column

    def valid_data_types(self):
        return ["integer", "float", "string"]

class DatasetTransformationClass(TestCase):
    def setUp(self):
        settings = AbstractSettings()
        self.dataset_transformation = IdentityTransformation(settings)

    def test_rotation_of_matrix(self):
        data_matrix = [
                [1,2,3,4],
                [5,6,7,8],
                [9,10,11,12]
                ]
        rotated_matrix = self.dataset_transformation.rotate_matrix(data_matrix)
        self.assertEqual(4, len(rotated_matrix))
        self.assertListEqual([1,5,9], rotated_matrix[0])
        self.assertListEqual([2,6,10], rotated_matrix[1])
        self.assertListEqual([3,7,11], rotated_matrix[2])
        self.assertListEqual([4,8,12], rotated_matrix[3])

    def test_identity_transform(self):
        data_matrix = [
                [1,2,3],
                [4,5,6]
                ]
        dataset = Dataset(data_matrix)

        transformed_dataset = self.dataset_transformation.transform(dataset)
        transformed_matrix, transformed_headers = transformed_dataset.data_matrix, transformed_dataset.headers
        self.assertEqual(2, len(transformed_matrix))
        self.assertListEqual([1,2,3], transformed_matrix[0])
        self.assertListEqual([4,5,6], transformed_matrix[1])
        self.assertEqual(None, transformed_headers)

    def test_identity_transform_with_headers(self):
        data_matrix = [
                [1,2,3],
                [4,5,6]
                ]
        headers = ["h0", "h1", "h2"]
        dataset = Dataset(data_matrix, headers)

        transformed_dataset = self.dataset_transformation.transform(dataset)
        transformed_matrix, transformed_headers = transformed_dataset.data_matrix, transformed_dataset.headers
        self.assertEqual(2, len(transformed_matrix))
        self.assertListEqual([1,2,3], transformed_matrix[0])
        self.assertListEqual([4,5,6], transformed_matrix[1])

        self.assertEqual(3, len(transformed_headers))
        self.assertEqual("identitytransformation_h0", transformed_headers[0])
        self.assertEqual("identitytransformation_h1", transformed_headers[1])
        self.assertEqual("identitytransformation_h2", transformed_headers[2])

    def test_appending_multiple_lists(self):
        data_matrix = []
        lists = [[1,3,"hello"],[2,3,"more"]]
        self.dataset_transformation.append_lists(data_matrix, lists)

        self.assertEqual(2, len(data_matrix))
        self.assertListEqual([1,3,"hello"], data_matrix[0])
        self.assertListEqual([2,3,"more"], data_matrix[1])

    def test_appending_single_list(self):
        data_matrix = []
        lists = ["more", 2.3, "bobby"]
        self.dataset_transformation.append_lists(data_matrix, lists)

        self.assertEqual(1, len(data_matrix))
        self.assertListEqual(["more", 2.3, "bobby"], data_matrix[0])

    def test_header_transformation_for_dataset_without_headers(self):
        data_matrix = [
                [1,2,3],
                [4,5,6]
                ]
        dataset = Dataset(data_matrix)
        variable = DatasetVariable(0)
        header = self.dataset_transformation.get_transformed_header(dataset, variable)

        self.assertEqual(None, header)

    def test_header_transformation_for_dataset_with_headers(self):
        data_matrix = [
                [1,2,3],
                [4,5,6]
                ]
        headers = ["h0", "h1", "h2"]
        dataset = Dataset(data_matrix, headers)

        variable = DatasetVariable(0)
        header = self.dataset_transformation.get_transformed_header(dataset, variable)
        self.assertEqual("identitytransformation_h0", header)

        variable = DatasetVariable("h2")
        header = self.dataset_transformation.get_transformed_header(dataset, variable)
        self.assertEqual("identitytransformation_h2", header)
