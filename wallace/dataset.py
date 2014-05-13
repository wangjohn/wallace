import random
from wallace.data_type_classification import DataTypeClassification
from wallace.data_type import DataType

class Dataset(object):
    def __init__(self, data_matrix, headers=None, data_types=None):
        self.headers = headers
        self.data_matrix = data_matrix
        self.num_rows = len(self.data_matrix)
        self.num_cols = len(self.data_matrix[0])
        self.data_types = self._initialize_data_types(data_types)

    def get(self, row, col):
        return self.data_matrix[row][col]

    def get_with_header(self, row, header):
        self._check_headers()
        col = self.column_from_header(header)
        return self.get(row, col)

    def get_independent_variables(self, dependent_variable):
        dependent_column = dependent_variable.get_column_index(self)
        independent_variables = []
        for j in xrange(self.num_cols):
            if j != dependent_column:
                if self.headers == None:
                    variable = j
                else:
                    variable = self.headers[j]
                independent_variables.append(DatasetVariable(variable))
        return independent_variables

    def column_index(self, header):
        self._check_headers()
        for i in xrange(len(self.headers)):
            if self.headers[i] == header:
                return i

        raise ValueError("Header '%s' does not exist in this dataset." % header)

    def get_column(self, col):
        column = []
        for row in xrange(self.num_rows):
            column.append(self.data_matrix[row][col])
        return column

    def get_filtered_data_types(self, variables):
        indices = self._variable_indices(variables)
        return [self.data_types[index] for index in indices]

    def get_filtered_matrix(self, variables):
        indices = self._variable_indices(variables)

        filtered_dataset = []
        for row in self.data_matrix:
            variable_row = []
            for j in indices:
                variable_row.append(row[j])
            filtered_dataset.append(variable_row)
        return filtered_dataset

    def get_filtered_column(self, variable):
        col = variable.get_column_index(self)
        return self.get_column(col)

    def get_column_with_header(self, header):
        self._check_headers()
        col = self.column_index(header)
        return self.get_column(col)

    def get_row(self, row):
        return self.data_matrix[row]

    def crossfold_partitions(self, num_partitions=10):
        rows_per_partition = self.num_rows // num_partitions

        shuffled = list(self.data_matrix)
        random.shuffle(shuffled)

        for i in xrange(num_partitions):
            test_start = i * rows_per_partition
            if i < num_partitions - 1:
                test_end = (i+1) * rows_per_partition
            else:
                test_end = self.num_rows

            training_dataset = Dataset(shuffled[:test_start] + shuffled[test_end:], self.headers, self.data_types)
            test_dataset = Dataset(shuffled[test_start:test_end], self.headers, self.data_types)
            yield (training_dataset, test_dataset)

    def _initialize_data_types(self, data_types):
        if data_types == None:
            resulting_types = DataTypeClassification.classify_row(self.data_matrix[0])
        else:
            if len(data_types) != self.num_cols:
                raise ValueError("The data_types lists must be the same length as the number of columns in the dataset.")

            resulting_types = []
            for data_type in data_types:
                if isinstance(data_type, str):
                    resulting_types.append(DataType(data_type))
                else:
                    resulting_types.append(data_type)

        for i in xrange(len(resulting_types)):
            if resulting_types[i].is_equal("string"):
                resulting_types[i] = DataType("string", categories=set(self.get_column(i)))

        return resulting_types

    def _variable_indices(self, variables):
        if len(variables) <= 0:
            raise ValueError("Must have a non-empty list of variables when filtering dataset.")

        indices = []
        for variable in variables:
            indices.append(variable.get_column_index(self))
        return sorted(indices)

    def _check_headers(self):
        if self.headers == None:
            raise ValueError("Headers are not defined on this dataset and cannot be used for accesses.")

class DatasetVariable(object):
    def __init__(self, variable):
        self.variable = variable

    def get_column_index(self, dataset):
        if isinstance(self.variable, int):
            if 0 <= self.variable and self.variable < dataset.num_cols:
                return self.variable
            else:
                raise ValueError("Variable is out of the range of the dataset.")
        else:
            return dataset.column_index(self.variable)
