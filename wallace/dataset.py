class Dataset(object):
    def __init__(self, data_matrix, headers=None):
        self.headers = headers
        self.data_matrix = data_matrix
        self.rows = len(self.data_matrix)

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
        for row in xrange(self.rows):
            yield self.data_matrix[row][col]

    def get_column_with_header(self, header):
        self._check_headers()
        col = self.column_index(header)
        return self.get_column(col)

    def get_row(self, row):
        return self.data_matrix[row]

    def _check_headers(self):
        if self.headers == None:
            raise ValueError("Headers are not defined on this dataset and cannot be used for accesses.")
