from unittest import TestCase

from wallace.settings import AbstractSettings
from wallace.initialization import WallaceInitialization
import os

from wallace.predictive_models.lasso_regression import LassoRegression
from wallace.predictive_models.ols_linear_regression import OLSLinearRegression
from wallace.predictive_models.random_forest_regression import RandomForestRegression
from wallace.predictive_models.ridge_regression import RidgeRegression

class InitializationTest(TestCase):
    def setUp(self):
        self.settings = AbstractSettings()

    def test_creating_predictive_model_generator(self):
        models = {
            LassoRegression: None,
            OLSLinearRegression: None,
            RandomForestRegression: None,
            RidgeRegression: None
            }
        generator = WallaceInitialization(self.settings).create_predictive_model_generator(models)
        self.assertEqual(4, len(generator.list_model_types()))

        for model_information in generator.list_model_types():
            self.assertEqual(2, len(model_information))
            self.assertIn("model_class", model_information)
            self.assertIn("parameter_validity_check", model_information)

    def test_running_initialization(self):
        settings = {"optimization_algorithm.finishing_criteria.max_steps": 1}
        dependent_variable = "IsBadBuy"
        dataset_filename = os.path.join(os.path.dirname(__file__), "example_dataset.csv")
        WallaceInitialization.initialize(settings, dependent_variable, dataset_filename)

    def test_read_filename(self):
        dataset_filename = os.path.join(os.path.dirname(__file__), "example_dataset.csv")
        dataset = WallaceInitialization(self.settings).read_filename(dataset_filename)

        self.assertEqual(18, dataset.num_rows)

        self.assertEqual(32, len(dataset.headers))
        self.assertEqual(32, dataset.num_cols)
        self.assertEqual("RefId", dataset.headers[0])
        self.assertEqual("IsBadBuy", dataset.headers[1])
        self.assertEqual("PurchDate", dataset.headers[2])
        self.assertEqual("Auction", dataset.headers[3])
        self.assertEqual("VehYear", dataset.headers[4])
        self.assertEqual("VehicleAge", dataset.headers[5])
        self.assertEqual("Make", dataset.headers[6])
        self.assertEqual("Model", dataset.headers[7])
        self.assertEqual("Trim", dataset.headers[8])
        self.assertEqual("SubModel", dataset.headers[9])
        self.assertEqual("Color", dataset.headers[10])
        self.assertEqual("Transmission", dataset.headers[11])
        self.assertEqual("WheelTypeID", dataset.headers[12])
        self.assertEqual("WheelType", dataset.headers[13])
        self.assertEqual("VehOdo", dataset.headers[14])
        self.assertEqual("Nationality", dataset.headers[15])
        self.assertEqual("Size", dataset.headers[16])
        self.assertEqual("TopThreeAmericanName", dataset.headers[17])
        self.assertEqual("MMRAcquisitionAuctionAveragePrice", dataset.headers[18])
        self.assertEqual("MMRAcquisitionAuctionCleanPrice", dataset.headers[19])
        self.assertEqual("MMRAcquisitionRetailAveragePrice", dataset.headers[20])
        self.assertEqual("MMRAcquisitonRetailCleanPrice", dataset.headers[21])
        self.assertEqual("MMRCurrentAuctionAveragePrice", dataset.headers[22])
        self.assertEqual("MMRCurrentAuctionCleanPrice", dataset.headers[23])
        self.assertEqual("MMRCurrentRetailAveragePrice", dataset.headers[24])
        self.assertEqual("MMRCurrentRetailCleanPrice", dataset.headers[25])
        self.assertEqual("BYRNO", dataset.headers[26])
        self.assertEqual("VNZIP1", dataset.headers[27])
        self.assertEqual("VNST", dataset.headers[28])
        self.assertEqual("VehBCost", dataset.headers[29])
        self.assertEqual("IsOnlineSale", dataset.headers[30])
        self.assertEqual("WarrantyCost", dataset.headers[31])

        self.assertEqual(32, len(dataset.data_types))
        self.assertEqual("integer", dataset.data_types[0].data_type)
        self.assertEqual("integer", dataset.data_types[1].data_type)
        self.assertEqual("date", dataset.data_types[2].data_type)
        self.assertEqual("string", dataset.data_types[3].data_type)
        self.assertEqual("integer", dataset.data_types[4].data_type)
        self.assertEqual("integer", dataset.data_types[5].data_type)
        self.assertEqual("string", dataset.data_types[6].data_type)
        self.assertEqual("string", dataset.data_types[7].data_type)
        self.assertEqual("string", dataset.data_types[8].data_type)
        self.assertEqual("string", dataset.data_types[9].data_type)
        self.assertEqual("string", dataset.data_types[10].data_type)
        self.assertEqual("string", dataset.data_types[11].data_type)
        self.assertEqual("integer", dataset.data_types[12].data_type)
        self.assertEqual("string", dataset.data_types[13].data_type)
        self.assertEqual("integer", dataset.data_types[14].data_type)
        self.assertEqual("string", dataset.data_types[15].data_type)
        self.assertEqual("string", dataset.data_types[16].data_type)
        self.assertEqual("string", dataset.data_types[17].data_type)
        self.assertEqual("integer", dataset.data_types[18].data_type)
        self.assertEqual("integer", dataset.data_types[19].data_type)
        self.assertEqual("integer", dataset.data_types[20].data_type)
        self.assertEqual("integer", dataset.data_types[21].data_type)
        self.assertEqual("integer", dataset.data_types[22].data_type)
        self.assertEqual("integer", dataset.data_types[23].data_type)
        self.assertEqual("integer", dataset.data_types[24].data_type)
        self.assertEqual("integer", dataset.data_types[25].data_type)
        self.assertEqual("integer", dataset.data_types[26].data_type)
        self.assertEqual("integer", dataset.data_types[27].data_type)
        self.assertEqual("string", dataset.data_types[28].data_type)
        self.assertEqual("integer", dataset.data_types[29].data_type)
        self.assertEqual("integer", dataset.data_types[30].data_type)
        self.assertEqual("integer", dataset.data_types[31].data_type)

