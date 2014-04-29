class PredictiveModel(object):
    def __init__(self, settings, parameter_set, dependent_variable, independent_variables):
        self.parameter_set = parameter_set
        self.settings = settings
        self.dependent_variable = dependent_variable
        self.independent_variables = independent_variables

    def train(self, dataset):
        raise NotImplementedError()

    def get_dependent_variable_data(self, dataset):
        return dataset.get_filtered_column(self.dependent_variable)

    def get_independent_variable_data(self, dataset):
        return dataset.get_filtered_matrix(self.independent_variables)

class TrainedPredictiveModel(object):
    def __init__(self, predictive_model):
        self.predictive_model = predictive_model

    def model_type(self):
        return self.predictive_model.__class__.__name__

    def predict(self, dataset):
        raise NotImplementedError()

    def predict_and_evaluate_fitness(self, dataset, evaluation_method):
        predicted_results = self.predict(dataset)
        actual_results = self.predictive_model.get_dependent_variable_data(dataset)
        return evaluation_method.evaluate_fitness(results, actual_results)
