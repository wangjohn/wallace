from datetime import datetime
from wallace.data_type_classification import DataTypeClassification
from wallace.data_type import DataType
import logging

class DatasetCleaner(object):
    def __init__(self, settings, data_matrix, headers=None, data_types=None):
        self.settings = settings
        self.data_matrix = data_matrix
        self.headers = headers
        self.logger = logging.getLogger(__name__)
        if data_types == None:
            self.data_types = DataTypeClassification.classify_data_matrix(self.data_matrix)
        else:
            self.data_types = data_types

    def clean(self):
        self.logger.info("Cleaning dataset.")
        if len(self.data_matrix) <= 0:
            return self.data_matrix

        num_columns = self.get_num_columns(self.data_matrix, self.headers)
        self.logger.info("Row data types: %s", str(self.data_types))

        resulting_data_matrix = []
        for i in xrange(len(self.data_matrix)):
            if len(self.data_matrix[i]) != num_columns:
                raise ValueError("Invalid data matrix. Number of columns is not static. See row %s." % i)

            self.clean_and_append_row(i, self.data_matrix, resulting_data_matrix)

        return self.handle_missing_data(resulting_data_matrix)

    def handle_missing_data(self, data_matrix):
        missing_data_points = self.compute_missing_data_points(data_matrix)

        rows_to_drop = []
        for column, missing_row_indices in missing_data_points.iteritems():
            if len(missing_row_indices) > 0:
                self._handle_missing_data_exception(column)

            missing_percentage = float(len(missing_row_indices)) / len(data_matrix)
            if missing_percentage < self.settings.get("dataset.maximum_missing_data_percentage"):
                rows_to_drop.extend(missing_row_indices)

        return self.drop_rows(set(rows_to_drop), data_matrix)

    def compute_missing_data_points(self, data_matrix):
        num_columns = self.get_num_columns(data_matrix, self.headers)
        missing_data_points = {}
        for j in xrange(num_columns):
            missing_data_points[j] = []

        for i in xrange(len(data_matrix)):
            for j in xrange(num_columns):
                if data_matrix[i][j] == None:
                    missing_data_points[j].append(i)

        return missing_data_points

    def drop_rows(self, rows_to_drop, data_matrix):
        resulting_data_matrix = []
        for i in xrange(len(data_matrix)):
            if i not in rows_to_drop:
                resulting_data_matrix.append(data_matrix[i])
        return resulting_data_matrix

    def _handle_missing_data_exception(self, column):
        if not self.settings.get("dataset.remove_rows_with_missing_data"):
            message = ("Invalid data matrix - contains missing data in column %s. "
                    "To remove rows with missing data instead of throwing an error, "
                    "set the `dataset.remove_rows_with_missing_data` setting to True.") % column
            raise ValueError(message)

    def get_num_columns(self, data_matrix, headers):
        if self.headers == None:
            return len(self.data_matrix[0])
        else:
            return len(self.headers)

    def clean_and_append_row(self, row_number, data_matrix, resulting_data_matrix):
        cleaned_row = []
        row = data_matrix[row_number]
        for column_number in xrange(len(row)):
            entry = row[column_number]
            cleaned_entry = self.clean_and_handle_entry(row_number, column_number, entry, resulting_data_matrix)
            cleaned_row.append(cleaned_entry)

        resulting_data_matrix.append(cleaned_row)

    def clean_and_handle_entry(self, row_number, column_number, entry, resulting_data_matrix):
        data_type = self.data_types[column_number]
        try:
            return self.clean_entry(entry, data_type)
        except ValueError:
            if data_type.is_equal("integer"):
                updated_type = DataType("float")
                self.update_data_type(row_number, column_number, updated_type, resulting_data_matrix)
                return self.clean_entry(entry, updated_type)
            else:
                raise ValueError("Dataset column %s has inconsistent data types.")

    def clean_entry(self, entry, data_type):
        if DataTypeClassification.is_missing_data(entry):
            return None
        elif data_type.is_equal("date"):
            return (DataTypeClassification.get_date(entry) - datetime(1970, 1, 1)).total_seconds()
        elif data_type.is_equal("integer"):
            return int(entry)
        elif data_type.is_equal("float"):
            return float(entry)

        return entry

    def update_data_type(self, row_number, column_number, updated_type, resulting_data_matrix):
        self.data_types[column_number] = updated_type
        if updated_type.is_equal("float"):
            for i in xrange(row_number):
                entry = resulting_data_matrix[i][column_number]
                resulting_data_matrix[i][column_number] = self.clean_entry(entry, updated_type)
