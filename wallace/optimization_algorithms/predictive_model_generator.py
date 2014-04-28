import random

from wallace.predictive_models import PredictiveModel

class PredictiveModelGenerator(object):
    def __init__(self, settings):
        self.settings = settings
        self.model_types = []

    def add_model_type(self, model_klass):
        if not issubclass(model_klass, PredictiveModel):
            raise ValueError("Model types added to the model generator must be subclasses of PredictiveModel.")
        if model_klass not in self.models:
            self.models.append(model_klass)

    def choose_model_type(self):
        return random.choice(self.model_types)
