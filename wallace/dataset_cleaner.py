from datetime import datetime
from wallace.data_type_classification import DataTypeClassification

class DatasetCleaner(object):
    def __init__(self, settings, data_matrix, headers=None):
        self.settings = settings
        self.data_matrix = data_matrix
        self.headers = headers

    def clean(self):
        if len(self.data_matrix) <= 0:
            return self.data_matrix

        num_columns = self.get_num_columns(self.data_matrix, self.headers)
        data_types = DataTypeClassification.classify_row(self.data_matrix[0])
        for i in xrange(len(self.data_matrix)):
            if len(self.data_matrix[i]) != num_columns:
                raise ValueError("Invalid data matrix. Number of columns is not static. See row %s." % i)

            try:
                cleaned_row = self.clean_row(self.data_matrix[i], data_types)
                self.data_matrix[i] = cleaned_row
            except MissingDataException:
                self._handle_missing_data_exception(i)

        return self.data_matrix

    def _handle_missing_data_exception(self, row_number):
        if not self.settings.get("dataset.remove_rows_with_missing_data"):
            message = ("Invalid data matrix - contains missing data in row %s. "
                    "To remove rows with missing data instead of throwing an error, "
                    "set the `dataset.remove_rows_with_missing_data` setting to True.") % row_number
            raise ValueError(message)

    def get_num_columns(self, data_matrix, headers):
        if self.headers == None:
            return len(self.data_matrix[0])
        else:
            return len(self.headers)

    def clean_row(self, row, data_types):
        cleaned_row = []
        for entry, data_type in zip(row, data_types):
            cleaned_entry = self.clean_entry(entry, data_type)
            cleaned_row.append(cleaned_entry)
        return cleaned_row

    def clean_entry(self, entry, data_type):
        if DataTypeClassification.is_missing_data(entry):
            raise MissingDataException()
        if data_type == "date":
            return (DataTypeClassification.get_date(entry) - datetime(1970, 1, 1)).total_seconds()

        return entry

class MissingDataException(Exception):
    pass
