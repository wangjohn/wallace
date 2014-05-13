from sklearn import preprocessing
from wallace.dataset_transformations.dataset_transformation import DatasetTransformation

import math

class SqrtTransformation(DatasetTransformation):
    def transform_column(self, column):
        return [math.sqrt(val) for val in column]

    def valid_data_types(self):
        return ["integer", "float"]

