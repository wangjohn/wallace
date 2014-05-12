from sklearn import preprocessing
from wallace.dataset_transformations.dataset_transformation import DatasetTransformation

import math

class LogTransformation(DatasetTransformation):
    DEFAULT_LOG_BASE = 10

    def transform_column(self, column):
        base = self.DEFAULT_LOG_BASE
        if self.settings.has("dataset_transformation.log_transformation_base")
            base = self.settings.get("dataset_transformation.log_transformation_base")

        return [math.log(val, base) for val in column]
