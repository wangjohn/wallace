import itertools

class Dataset(object):
    def __init__(self, data_matrix, headers=None):
        self.headers = headers
        self.data_matrix = data_matrix
        self.num_rows = len(self.data_matrix)
        self.num_cols = len(self.headers)

    def get(self, row, col):
        return self.data_matrix[row][col]

    def get_with_header(self, row, header):
        self._check_headers()
        col = self.column_from_header(header)
        return self.get(row, col)

    def column_index(self, header):
        for i in xrange(len(self.headers)):
            if self.headers[i] == header:
                return i

    def get_column(self, col):
        for row in xrange(self.num_rows):
            yield self.data_matrix[row][col]

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

    def _check_headers(self):
        if self.headers == None:
            raise ValueError("Headers are not defined on this dataset and cannot be used for accesses.")
