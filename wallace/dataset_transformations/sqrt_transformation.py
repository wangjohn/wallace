from sklearn import preprocessing
from wallace.dataset_transformations.dataset_transformation import DatasetTransformation

import math

class SqrtTransformation(DatasetTransformation):
    def transform_column(self, column):
        try:
            return [math.sqrt(val) for val in column]
        except ValueError:
            return None
