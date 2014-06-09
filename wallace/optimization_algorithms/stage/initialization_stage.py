from optimization_algorithm_stage import OptimizationAlgorithmStage
from wallace.optimization_algorithms.predictive_model_generator import PredictiveModelGenerator
from wallace.predictive_models.ols_linear_regression import OLSLinearRegression

class InitializationStage(OptimizationAlgorithmStage):

    INITIALIZATION_MODEL_TYPES = {
        OLSLinearRegression: 1.0
        }

    def __init__(self, settings):
        self.settings = settings

    def on_step(self, payload=None):
        if "optimization_algorithm" in payload:
            optimization_algorithm = payload["optimization_algorithm"]

            real_predictive_model_generator = optimization_algorithm.predictive_model_generator
            temporary_model_generator = self.create_temporary_model_generator()
            optimization_algorithm.predictive_model_generator = temporary_model_generator
            optimization_algorithm.update_population()

            optimization_algorithm.predictive_model_generator = real_predictive_model_generator

    def create_temporary_model_generator(self):
        predictive_model_generator = PredictiveModelGenerator(self.settings)
        predictive_model_generator.set_model_types(self.INITIALIZATION_MODEL_TYPES)
        return predictive_model_generator
