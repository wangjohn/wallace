from unittest import TestCase

from wallace.data_type_classification import DataTypeClassification

class DataTypeClassificationTest(TestCase):
    def test_date_classification(self):
        self.assertEqual(True, DataTypeClassification.is_date("25/3/1992"))
        self.assertEqual(True, DataTypeClassification.is_date("3/14/1942"))
        self.assertEqual(True, DataTypeClassification.is_date("10-2-2010"))
        self.assertEqual(True, DataTypeClassification.is_date("29-3-2014"))
        self.assertEqual(True, DataTypeClassification.is_date("1-1-11"))
        self.assertEqual(True, DataTypeClassification.is_date("15-1-03"))
        self.assertEqual(True, DataTypeClassification.is_date("4/23/95"))
        self.assertEqual(True, DataTypeClassification.is_date("23/2/42"))

        self.assertEqual(False, DataTypeClassification.is_date("52-3-3413"))
        self.assertEqual(False, DataTypeClassification.is_date("1-3-1"))
        self.assertEqual(False, DataTypeClassification.is_date("52-3-22"))
        self.assertEqual(False, DataTypeClassification.is_date("2-43-53"))
        self.assertEqual(False, DataTypeClassification.is_date("13-13-53"))
        self.assertEqual(False, DataTypeClassification.is_date("13/13/53"))
        self.assertEqual(False, DataTypeClassification.is_date("1/1/3"))

    def test_is_integer(self):
        self.assertEqual(True, DataTypeClassification.is_integer("1"))
        self.assertEqual(True, DataTypeClassification.is_integer("1435"))
        self.assertEqual(True, DataTypeClassification.is_integer("143523452345234523452345234523452345234523452345"))
        self.assertEqual(True, DataTypeClassification.is_integer("-234"))

        self.assertEqual(False, DataTypeClassification.is_integer("0."))
        self.assertEqual(False, DataTypeClassification.is_integer("-2.54"))
        self.assertEqual(False, DataTypeClassification.is_integer("-something"))
        self.assertEqual(False, DataTypeClassification.is_integer("5s3"))

    def test_is_float(self):
        self.assertEqual(True, DataTypeClassification.is_float("1."))
        self.assertEqual(True, DataTypeClassification.is_float("1435.345"))
        self.assertEqual(True, DataTypeClassification.is_float("143523452345234523452345234523452345234523.452345"))
        self.assertEqual(True, DataTypeClassification.is_float("-.234"))
        self.assertEqual(True, DataTypeClassification.is_float("5"))

        self.assertEqual(False, DataTypeClassification.is_float("-2.54shc"))
        self.assertEqual(False, DataTypeClassification.is_float("-something"))
        self.assertEqual(False, DataTypeClassification.is_float("5s3"))

    def test_is_boolean(self):
        self.assertEqual(True, DataTypeClassification.is_boolean("t"))
        self.assertEqual(True, DataTypeClassification.is_boolean("T"))
        self.assertEqual(True, DataTypeClassification.is_boolean("true"))
        self.assertEqual(True, DataTypeClassification.is_boolean("True"))
        self.assertEqual(True, DataTypeClassification.is_boolean("TRUE"))
        self.assertEqual(True, DataTypeClassification.is_boolean("f"))
        self.assertEqual(True, DataTypeClassification.is_boolean("F"))
        self.assertEqual(True, DataTypeClassification.is_boolean("false"))
        self.assertEqual(True, DataTypeClassification.is_boolean("False"))
        self.assertEqual(True, DataTypeClassification.is_boolean("FALSE"))

        self.assertEqual(False, DataTypeClassification.is_boolean("tru"))
        self.assertEqual(False, DataTypeClassification.is_boolean("fals"))
        self.assertEqual(False, DataTypeClassification.is_boolean("0"))
        self.assertEqual(False, DataTypeClassification.is_boolean("1."))

    def test_is_missing_data(self):
        self.assertEqual(True, DataTypeClassification.is_missing_data("NA"))
        self.assertEqual(True, DataTypeClassification.is_missing_data("NAN"))
        self.assertEqual(True, DataTypeClassification.is_missing_data("NaN"))
        self.assertEqual(True, DataTypeClassification.is_missing_data("nan"))
        self.assertEqual(True, DataTypeClassification.is_missing_data("null"))
        self.assertEqual(True, DataTypeClassification.is_missing_data("NULL"))
        self.assertEqual(True, DataTypeClassification.is_missing_data("na"))

        self.assertEqual(False, DataTypeClassification.is_missing_data("nope"))
        self.assertEqual(False, DataTypeClassification.is_missing_data("-"))
        self.assertEqual(False, DataTypeClassification.is_missing_data("5"))
        self.assertEqual(False, DataTypeClassification.is_missing_data("something"))

    def test_classification(self):
        self.assertEqual("integer", DataTypeClassification.classify("23452224"))
        self.assertEqual("float", DataTypeClassification.classify("234.52224"))
        self.assertEqual("date", DataTypeClassification.classify("3/20/1994"))
        self.assertEqual("boolean", DataTypeClassification.classify("t"))
        self.assertEqual("boolean", DataTypeClassification.classify("False"))
        self.assertEqual("string", DataTypeClassification.classify("be"))
        self.assertEqual("string", DataTypeClassification.classify("alfred"))

    def test_parsing_data_types_correctly_for_strings(self):
        row = ["some string", "2string", "string24531234 34534 345", "2.345s"]
        data_types = DataTypeClassification.classify_row(row)
        self.assertEqual("string", data_types[0])
        self.assertEqual("string", data_types[1])
        self.assertEqual("string", data_types[2])
        self.assertEqual("string", data_types[3])

    def test_parsing_data_types_correctly_for_ints_and_floats(self):
        row = ["1234", "  34.231 ", " 32. 43 ", " 5399999999999999 ", "23452345234523452345245.24"]
        data_types = DataTypeClassification.classify_row(row)
        self.assertEqual("integer", data_types[0])
        self.assertEqual("float", data_types[1])
        self.assertEqual("string", data_types[2])
        self.assertEqual("integer", data_types[3])
        self.assertEqual("float", data_types[4])

    def test_parsing_data_types_correctly_for_bools(self):
        row = ["t", "true", "True", "TRUE", "f", "false", "False", "FALSE"]
        data_types = DataTypeClassification.classify_row(row)
        self.assertEqual("boolean", data_types[0])
        self.assertEqual("boolean", data_types[1])
        self.assertEqual("boolean", data_types[2])
        self.assertEqual("boolean", data_types[3])
        self.assertEqual("boolean", data_types[4])
        self.assertEqual("boolean", data_types[5])
        self.assertEqual("boolean", data_types[6])
        self.assertEqual("boolean", data_types[7])

