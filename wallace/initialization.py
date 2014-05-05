from settings import AbstractSettings

from weighted_selection import WeightedSelection

from wallace.predictive_models.lasso_regression import LassoRegression
from wallace.predictive_models.ols_linear_regression import OLSLinearRegression
from wallace.predictive_models.ridge_regression import RidgeRegression

class WallaceInitialization(object):

    DEFAULT_PREDICTIVE_MODELS = {
            LassoRegression: None,
            OLSLinearRegression: None,
            RidgeRegression: None
        }

    def __init__(self, settings, models=None):
        self.settings = AbstractSettings(settings)
        self.models = models

    def create_predictive_model_generator(self, models=None):
        if models == None:
            models = WeightedSelection(DEFAULT_PREDICTIVE_MODELS).normalize_weights()
        elif isinstance(models, list):
            predictive_models = {}
            for model in models:
                predictive_models[model] = None
            models = WeightedSelection(predictive_models).normalize_weights()
        else:
            models = WeightedSelection(models).normalize_weights()

