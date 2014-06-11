from wallace import dataset
from datetime import datetime
import logging

class FitnessEvaluation(object):
    def __init__(self, settings, model, dataset):
        self.settings = settings
        self.model = model
        self.dataset = dataset

    def evaluate(self, evaluation_method):
        raise NotImplementedError()

class CrossValidationFitnessEvaluation(FitnessEvaluation):
    def __init__(self, settings, model, dataset):
        FitnessEvaluation.__init__(self, settings, model, dataset)
        self.logger = logging.getLogger(__name__)

    def evaluate(self, evaluation_method):
        num_partitions = self.settings.get("fitness_evaluation.crossfold_partitions")
        averaged_fitness = 0
        for training_dataset, test_dataset in self.dataset.crossfold_partitions(num_partitions):
            start_training = datetime.now()
            trained_model = self.model.train(training_dataset)
            finished_training = datetime.now()
            self.logger.debug("Training model time %s", (finished_training - start_training).total_seconds())

            fitness = trained_model.predict_and_evaluate_fitness(test_dataset, evaluation_method)
            finished_evaluating_fitness = datetime.now()
            self.logger.debug("Fitness evaluation time %s", (finished_evaluating_fitness - finished_training).total_seconds())

            self.logger.debug("Crossfold partition fitness for model %s: %s", self.model, fitness)
            averaged_fitness += (float(test_dataset.num_rows) / (test_dataset.num_rows + training_dataset.num_rows)) * fitness
        return averaged_fitness
