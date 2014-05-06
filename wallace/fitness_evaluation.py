from wallace import dataset

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

    def evaluate(self, evaluation_method):
        num_partitions = self.settings.get("fitness_evaluation.crossfold_partitions")
        averaged_fitness = 0
        for training_dataset, test_dataset in self.dataset.crossfold_partitions(num_partitions):
            trained_model = model.train(training_dataset)
            fitness = model.predict_and_evaluate_fitness(test_dataset, evaluation_method)

            averaged_fitness += (float(test_dataset.num_rows) / training_dataset.num_rows) * fitness
        return averaged_fitness
