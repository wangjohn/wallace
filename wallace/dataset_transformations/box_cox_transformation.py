from sklearn import preprocessing
from scipy import stats
from wallace.dataset_transformations.dataset_transformation import DatasetTransformation
import numpy

class BoxCoxTransformation(DatasetTransformation):
    def transform_column(self, column):
        array = numpy.array(column)
        np_array_result, _ = stats.boxcox(array)
        return np_array_result.tolist()

    def valid_data_types(self):
        return ["integer", "float"]
