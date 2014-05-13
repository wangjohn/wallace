from sklearn import preprocessing
from wallace.dataset_transformations.dataset_transformation import DatasetTransformation

class ScaleTransformation(DatasetTransformation):
    def transform_column(self, column):
        float_column = [float(i) for i in column]
        return preprocessing.scale(float_column)

    def valid_data_types(self):
        return ["integer", "float"]

