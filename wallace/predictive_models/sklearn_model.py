from sklearn import preprocessing

from wallace.predictive_models.predictive_model import PredictiveModel, TrainedPredictiveModel

class SklearnModel(PredictiveModel):
    def get_dependent_variable_data(self, dataset):
        dependent_column = dataset.get_filtered_column(self.dependent_variable)
        encoder = self.get_encoder(dataset)
        return encoder.transform(dependent_column)

    def get_independent_variable_data(self, dataset):
        filtered_matrix = dataset.get_filtered_matrix(self.independent_variables)
        encoder = self.get_encoder(dataset)
        return encoder.fit(filtered_matrix)

    def get_encoder(self, dataset):
        filtered_data_types = dataset.get_filtered_data_types(self.independent_variables)
        categorical_features = []
        for i in xrange(len(filtered_data_types)):
            data_type = filtered_data_types[i]
            if data_type == "string" or data_type == "boolean":
                categorical_features.append(i)

        return preprocessing.OneHotEncoder(categorical_features=categorical_features)

class TrainedSklearnModel(TrainedPredictiveModel):
    def __init__(self, predictive_model, fitted_regression):
        TrainedPredictiveModel.__init__(self, predictive_model)
        self.fitted_regression = fitted_regression

    def predict(self, dataset):
        independent_data = self.predictive_model.get_independent_variable_data(dataset)
        return self.fitted_regression.predict(independent_data)
