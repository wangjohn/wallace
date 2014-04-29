from sklearn import linear_model
from wallace.predictive_models.predictive_model import PredictiveModel, TrainedSklearnModel

class RidgeRegression(PredictiveModel):
    def train(self, dataset):
        model = linear_model.Ridge(alpha=self.get_alpha())
        independent_data = self.get_independent_variable_data(dataset)
        dependent_data = self.get_dependent_variable_data(dataset)
        trained_regression = model.fit(independent_data, dependent_data)

        return TrainedSklearnModel(self, trained_regression)

    def get_alpha(self):
        return self.parameter_set.get("ridge_regression_alpha")
