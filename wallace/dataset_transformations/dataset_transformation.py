from wallace.dataset import Dataset, DatasetVariable

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

            current_transformed = self.transform_column(current_column)
            self.append_lists(transformed_columns, current_transformed)

        if dataset.headers == None:
            headers = None
        else:
            headers = []
            for j in xrange(num_cols):
                transformed_header = self.get_transformed_header(dataset, variables[j])
                headers.append(transformed_header)

        data_matrix = self.rotate_matrix(transformed_columns)
        return Dataset(data_matrix, headers)

    def get_transformed_header(self, dataset, variable):
        if dataset.headers == None:
            return None
        else:
            column_index = variable.get_column_index(dataset)
            class_name = self.__class__.__name__.lower()
            data_header = dataset.headers[column_index]
            return "%s_%s" % (class_name, data_header)

    def append_lists(self, data_matrix, lists):
        is_single_list = False
        for element in lists:
            if isinstance(element, list):
                data_matrix.append(element)
            else:
                is_single_list = True
                break

        if is_single_list:
            data_matrix.append(lists)

    def rotate_matrix(self, data_matrix):
        num_cols = len(data_matrix[0])
        rotated_matrix = []
        for j in xrange(num_cols):
            current_row = []
            for i in xrange(len(data_matrix)):
                current_row.append(data_matrix[i][j])
            rotated_matrix.append(current_row)

        return rotated_matrix

    def transform_column(self, column):
        raise NotImplementedError()
