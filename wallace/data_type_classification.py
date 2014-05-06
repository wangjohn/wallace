from datetime import datetime

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
        lowercased = obj.strip().lower()
        return lowercased in ["nan", "null", "na", ""]

    @classmethod
    def is_date(klass, entry):
        for date_format in klass.VALID_DATE_FORMATS:
            try:
                datetime.strptime(entry, date_format)
                return True
            except ValueError:
                pass
        return False

    @classmethod
    def classify(klass, entry):
        if klass.is_integer(entry):
            return "integer"
        elif klass.is_float(entry):
            return "float"
        elif klass.is_boolean(entry):
            return "boolean"
        elif klass.is_date(entry):
            return "date"
        else:
            return "string"

    @classmethod
    def classify_row(klass, row):
        return [klass.classify(entry) for entry in row]

