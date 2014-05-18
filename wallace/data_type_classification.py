from datetime import datetime
from wallace.data_type import DataType

class DataTypeClassification(object):
    VALID_DATE_FORMATS = [
            "%m/%d/%y",
            "%m-%d-%y",
            "%d/%m/%y",
            "%d-%m-%y",
            "%m/%d/%Y",
            "%m-%d-%Y",
            "%d/%m/%Y",
            "%d-%m-%Y"
            ]

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
        if obj == None:
            return True
        lowercased = obj.strip().lower()
        return lowercased in ["nan", "null", "na", ""]

    @classmethod
    def is_date(klass, entry):
        return klass.get_date(entry) != None

    @classmethod
    def get_date(klass, entry):
        for date_format in klass.VALID_DATE_FORMATS:
            try:
                return datetime.strptime(entry, date_format)
            except ValueError:
                pass

    @classmethod
    def classify(klass, entry):
        if klass.is_integer(entry):
            return DataType("integer")
        elif klass.is_float(entry):
            return DataType("float")
        elif klass.is_boolean(entry):
            return DataType("boolean")
        elif klass.is_date(entry):
            return DataType("date")
        else:
            return DataType("string")

    @classmethod
    def classify_row(klass, row):
        return [klass.classify(entry) for entry in row]
