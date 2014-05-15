from wallace.settings import AbstractSettings
from wallace.weighted_selection import WeightedSelection
from wallace.dataset import DatasetVariable
from wallace.dataset_file_reader import DatasetFileReader
from wallace.optimization_algorithms.predictive_model_generator import PredictiveModelGenerator
from wallace.dataset_transformations.dataset_transformer import DatasetTransformer
from multiprocessing import Pool
import logging

from wallace.predictive_models.lasso_regression import LassoRegression
from wallace.predictive_models.ols_linear_regression import OLSLinearRegression
from wallace.predictive_models.ridge_regression import RidgeRegression

from wallace.optimization_algorithms.differential_evolution import DifferentialEvolution

class WallaceInitialization(object):

    DEFAULT_PREDICTIVE_MODELS = {
            LassoRegression: None,
            OLSLinearRegression: None,
            RidgeRegression: None
        }

    def __init__(self, settings, models=None):
        if isinstance(settings, AbstractSettings):
            self.settings = settings
        else:
            self.settings = AbstractSettings(settings)
        self.models = models
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Wallace.")

    def create_predictive_model_generator(self, models=None):
        if models == None:
            models = WeightedSelection(self.DEFAULT_PREDICTIVE_MODELS).normalize_weights()
        elif isinstance(models, list):
            predictive_models = {}
            for model in models:
                predictive_models[model] = None
            models = WeightedSelection(predictive_models).normalize_weights()
        else:
            models = WeightedSelection(models).normalize_weights()

        predictive_model_generator = PredictiveModelGenerator(self.settings)
        predictive_model_generator.set_model_types(models)

        return predictive_model_generator

    def run_differential_evolution(self, dataset, dependent_variable):
        self.logger.info("Running differential evolution on dataset.")
        predictive_model_generator = self.create_predictive_model_generator()
        differential_evolution = DifferentialEvolution(dataset, dependent_variable, self.settings, predictive_model_generator)
        differential_evolution.run()

    def read_filename(self, dataset_filename):
        dataset = DatasetFileReader(self.settings, dataset_filename).read()
        if self.settings.get("dataset_transformation.transform_datasets"):
            return self.clean_and_transform_data(dataset)
        else:
            return dataset

    def clean_and_transform_data(self, dataset):
        return DatasetTransformer(self.settings).transform(dataset)

    @classmethod
    def initialize(klass, settings, dependent_variable, dataset_filename):
        initialization = WallaceInitialization(settings)
        initialization.settings.set("dataset.dataset_filename", dataset_filename)
        dataset = initialization.read_filename(dataset_filename)

        if not isinstance(dependent_variable, DatasetVariable):
            dependent_variable = DatasetVariable(dependent_variable)

        initialization.run_differential_evolution(dataset, dependent_variable)

    @classmethod
    def initialize_multiprocess_pool(klass, settings, dependent_variable, dataset_filename, processes=10):
        pool = Pool(processes=processes)
        result = pool.apply_async(klass.initialize, args=(settings, dependent_variable, dataset_filename))
