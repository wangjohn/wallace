import itertools

class Dataset(object):
    def __init__(self, data_matrix, headers=None):
        self.headers = headers
        self.data_matrix = data_matrix
        self.num_rows = len(self.data_matrix)
        self.num_cols = len(self.data_matrix[0])

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

        raise ValueError("Header '%s' does not exist in this dataset.")

    def get_column(self, col):
        column = []
        for row in xrange(self.num_rows):
            column.append(self.data_matrix[row][col])
        return column

    def get_filtered_matrix(self, variables):
        indices = []
        for variable in variables:
            indices.append(variable.get_column_index(self))
        indices = sorted(indices)

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

            training_dataset = Dataset(shuffled[:start] + shuffled[end:])
            test_dataset = Dataset(shuffled[start:end], self.headers)
            yield (training_dataset, test_dataset)

    @classmethod
    def read_filename(klass, dataset_filename):
        raise NotImplementedError()

    def _check_headers(self):
        if self.headers == None:
            raise ValueError("Headers are not defined on this dataset and cannot be used for accesses.")

import csv

class DatasetFileReader(object):
    def __init__(self, settings, dataset_filename):
        self.settings = settings
        self.dataset_filename = dataset_filename

    def read(self, maximum_size=None, delimiter=",", quoting=csv.QUOTE_NONE):
        if maximum_size == None:
            maximum_size = self.settings.get("dataset.maximum_dataset_size")

        with open(self.dataset_filename, 'rb') as f:
            reader = csv.reader(f, delimiter=delimiter, quoting=quoting)
            if self.settings.get("dataset.randomize_file_reader"):
                data_matrix = self.randomized_read_lines(csv_reader, maximum_size)
            else:
                data_matrix = self.greedy_read_lines(reader, maximum_size)

        data_matrix, headers = self.detect_headers(data_matrix)
        return Dataset(data_matrix, headers=headers)

    def detect_headers(self, data_matrix):
        """
        We look to see if there are any headers in the first row of the data_matrix.
        We check to make sure that all data types in the first row are either strings
        or booleans (because booleans can have "t", "true", etc. which could
        potentially be a header).

        If all data types in the first row are either strings or booleans, we check
        to make sure that the second row does not match exactly the first row. If
        both rows match, then we assume there were no headers. Otherwise we return
        the first row as headers.
        """
        header_data_types = self.parse_data_type(data_matrix[0])
        row_data_types = self.parse_data_type(data_matrix[1])

        non_matching_types = 0
        for header_type, row_type in zip(header_data_types, row_data_types):
            if header_type in [bool, str]:
                if header_type != row_type:
                    non_matching_types += 1
            else:
                # Header type is not a boolean or string --  we assume that
                # this data_matrix doesn't have any headers.
                return (data_matrix, None)

        # If all header and first row types are matching, then we assume we don't
        # have any headers. Otherwise, we return the first row as headers.
        if non_matching_types == 0:
            return (data_matrix, None)
        else:
            headers = data_matrix.pop(0)
            return (data_matrix, headers)

    def parse_data_type(self, row):
        data_types = []
        for entry in row:
            if DataTypeClassification.is_integer(entry):
                data_types.append(int)
            elif DataTypeClassification.is_float(entry):
                data_types.append(float)
            elif DataTypeClassification.is_boolean(entry):
                data_types.append(bool)
            else:
                data_types.append(str)
        return data_types

    def greedy_read_lines(self, csv_reader, maximum_size):
        data_matrix = []
        for row in csv_reader:
            data_matrix.append(row)

            if len(data_matrix) >= maximum_size:
                break

        return data_matrix

    def randomized_read_lines(self, csv_reader, maximum_size):
        data_matrix = []
        count = 0
        for row in csv_reader:
            count += 1
            if count >= maximum_size:
                if random.random() < (float(maximum_size) / count):
                    replaced_index = random.randrange(maximum_size)
                    data_matrix[replaced_index] = row
            else:
                data_matrix.append(row)
        return data_matrix

class DataTypeClassification(object):
    @classmethod
    def is_integer(klass, obj):
        try:
            int(obj)
            return True
        except ValueError:
            return False

    @classmethod
    def is_float(klass, obj):
        try:
            float(obj)
            return True
        except ValueError:
            return False

    @classmethod
    def is_boolean(klass, obj):
        lowercased = obj.strip().lower()
        return lowercased in ["true", "t", "false", "f"]

    @classmethod
    def is_missing_data(klass, obj):
        lowercased = obj.strip().lower()
        return lowercased in ["nan", "null", "na", ""]

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
