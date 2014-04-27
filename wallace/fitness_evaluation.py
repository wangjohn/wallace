from wallace import dataset

class FitnessEvaluation(object):
    def __init__(self, settings, model, dataset):
        self.settings = settings
        self.model = model
        self.dataset = dataset

    def evaluate(self):
        raise NotImplementedError()

class CrossValidationFitnessEvaluation(FitnessEvaluation):
    def __init__(self, settings, model, dataset):
        FitnessEvaluation.__init__(self, settings, model, dataset)

    def evaluate(self, num_partitions=10):
        for training_dataset, test_dataset in self.dataset.crossfold_partitions(num_partitions):
            trained_model = model.train(training_dataset)
            predictions = model.predict(test_dataset)

            
