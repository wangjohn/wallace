from unittest import TestCase
import tempfile

from wallace.optimization_algorithms.optimization_algorithm_tracking import OptimizationAlgorithmTracking
from wallace.settings import AbstractSettings
from wallace.optimization_algorithms.predictive_model_generator import PredictiveModelGenerator
from wallace.predictive_models.predictive_model import PredictiveModel
from wallace.parameters import ParametersGeneralValidityCheck
from wallace.dataset import Dataset, DatasetVariable
from wallace.optimization_algorithms.optimization_algorithm import OptimizationAlgorithm

class FakePredictiveModel(PredictiveModel):
    @classmethod
    def validity_check(klass):
        validity_check = ParametersGeneralValidityCheck()
        validity_check.set_range_parameter("range_param_0", 0.0, 1.0)
        validity_check.set_range_parameter("range_param_1", 0.0, 1.0)
        validity_check.set_range_parameter("range_param_2", 0.0, 1.0)
        validity_check.set_category_parameter("category_param_0", ["0","1","2","3"])
        validity_check.set_category_parameter("category_param_1", ["0","1","2","3"], [0.1, 0.1, 0.3, 0.5])
        return validity_check

class OptimizationAlgorithmTrackingTest(TestCase):
    def setUp(self):
        settings = AbstractSettings({
            "optimization_algorithm.population_size": 5
        })
        predictive_model_generator = PredictiveModelGenerator(settings)
        predictive_model_generator.add_model_type(FakePredictiveModel)
        data_matrix = [[1,2,3,4], [2,3,4,5], [3,4,5,6], [0,1,3,4]]
        dataset = Dataset(data_matrix)
        dependent_variable = DatasetVariable(0)

        optimization_algorithm = OptimizationAlgorithm(dataset, dependent_variable, settings, predictive_model_generator)
        optimization_algorithm.initialize_population()
        self.model_population = optimization_algorithm.model_population

    def test_writing_tracking_history_to_file(self):
        temporary_file = tempfile.NamedTemporaryFile()
        settings = AbstractSettings({
            "optimization_algorithm_tracking.tracking_log_filename": temporary_file.name
            })

        tracking = OptimizationAlgorithmTracking(settings)
        tracking.track_step(0, self.model_population)

