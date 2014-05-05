class PredictiveModel(object):
    def __init__(self, settings, parameter_set, dependent_variable, independent_variables):
        self.parameter_set = parameter_set
        self.settings = settings
        self.dependent_variable = dependent_variable
        self.independent_variables = independent_variables

        self._validate_parameter_set(self.parameter_set)

    def train(self, dataset):
        raise NotImplementedError()

    def get_dependent_variable_data(self, dataset):
        return dataset.get_filtered_column(self.dependent_variable)

    def get_independent_variable_data(self, dataset):
        return dataset.get_filtered_matrix(self.independent_variables)

    @classmethod
    def required_parameters(self):
        return []

    def _validate_parameter_set(self, parameter_set):
        for parameter in self.required_parameters():
            if not parameter_set.has_parameter(parameter):
                raise AssertionError("The model's parameter set does not have the required parameter '%s'." % parameter)

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

class TrainedSklearnModel(TrainedPredictiveModel):
    def __init__(self, predictive_model, fitted_regression):
        TrainedPredictiveModel.__init__(self, predictive_model)
        self.fitted_regression = fitted_regression

    def predict(self, dataset):
        independent_data = self.predictive_model.get_independent_variable_data(dataset)
        return self.fitted_regression.predict(independent_data)
