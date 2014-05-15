class DataType(object):
    VALID_DATA_TYPES = [
            "integer",
            "float",
            "boolean",
            "date",
            "string"
        ]


    def __init__(self, data_type, categories=None):
        self.categories = categories
        if data_type in self.VALID_DATA_TYPES:
            self.data_type = data_type
        else:
            raise ValueError("Data type '%s' is not a valid data type." % data_type)

    def in_categories(self, data_value):
        if self.data_type != "string":
            raise ValueError("Categories are only valid for 'string' data types.")

        return (data_value in self.categories)

    def is_equal(self, data_type):
        return self.data_type == data_type

    def __str__(self):
        return self.data_type

    def __repr__(self):
        return self.__str__()
