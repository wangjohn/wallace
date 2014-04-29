from sklearn import linear_model
from wallace.predictive_models.predictive_model import PredictiveModel, TrainedPredictiveModel

class OLSLinearRegression(PredictiveModel):
    def train(self, dataset):
        model = linear_model.LinearRegression()
        independent_data = self.get_independent_variable_data(dataset)
        dependent_data = self.get_dependent_variable_data(dataset)
        trained_regression = model.fit(independent_data, dependent_data)

        return TrainedOLSLinearRegression(self, trained_regression)

class TrainedOLSLinearRegression(TrainedPredictiveModel):
    def __init__(self, predictive_model, fitted_regression):
        TrainedPredictiveModel.__init__(self, predictive_model)
        self.fitted_regression = fitted_regression

    def predict(self, dataset):
        independent_data = self.predictive_model.get_independent_variable_data(dataset)
        return self.fitted_regression.predict(independent_data)


