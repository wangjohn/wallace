from wallace.dataset import DatasetVariable

class DatasetTransformation(object):
    def __init__(self, settings):
        self.settings = settings

    def transform(self, dataset, variables=None):
        if variables == None:
            variables = [DatasetVariable(i) for i in xrange(dataset.num_cols)]

        filtered_matrix = dataset.get_filtered_matrix(variables)
        num_cols = len(filtered_matrix[0])
        transformed_columns = []
        for j in xrange(num_cols):
            current_column = []
            for i in xrange(len(filtered_matrix)):
                current_column.append(filtered_matrix[i][j])

            current_transformed = self.transform_column(column)
            transformed_columns.extend(current_transformed)

        return self.rotate_matrix(transformed_columns)

    def rotate_matrix(self, data_matrix):
        pass

    def transform_column(self, column):
        raise NotImplementedError()
