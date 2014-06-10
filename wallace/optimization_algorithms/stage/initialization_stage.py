from optimization_algorithm_stage import OptimizationAlgorithmStage
from wallace.optimization_algorithms.predictive_model_generator import PredictiveModelGenerator
from wallace.predictive_models.ols_linear_regression import OLSLinearRegression

from copy import deepcopy

class InitializationStage(OptimizationAlgorithmStage):

    INITIALIZATION_MODEL_TYPES = {
        OLSLinearRegression: 1.0
        }

    def __init__(self, settings):
        self.settings = settings

    def on_step(self, payload=None):
        optimization_algorithm = self._get_optimization_algorithm(payload)

        real_predictive_model_generator = optimization_algorithm.predictive_model_generator
        temporary_model_generator = self.create_temporary_model_generator(real_predictive_model_generator)
        optimization_algorithm.predictive_model_generator = temporary_model_generator

        if optimization_algorithm.current_step == 1:
            optimization_algorithm.initialize_population()
        optimization_algorithm.update_population()

        optimization_algorithm.predictive_model_generator = real_predictive_model_generator

    def create_temporary_model_generator(self, real_predictive_model_generator):
        predictive_model_generator = PredictiveModelGenerator(self.settings)

        model_types = deepcopy(self.INITIALIZATION_MODEL_TYPES)
        for model_type_wrapper in real_predictive_model_generator.list_model_types():
            model_class = model_type_wrapper["model_class"]
            if model_class not in model_types:
                model_types[model_class] = 0.0

        predictive_model_generator.set_model_types(model_types)
        return predictive_model_generator
