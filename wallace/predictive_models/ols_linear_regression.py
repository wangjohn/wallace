from sklearn import linear_model
from wallace.predictive_models.sklearn_model import SklearnModel, TrainedSklearnModel

class OLSLinearRegression(SklearnModel):
    def train(self, dataset):
        model = linear_model.LinearRegression()
        independent_data = self.get_independent_variable_data(dataset)
        dependent_data = self.get_dependent_variable_data(dataset)
        trained_regression = model.fit(independent_data, dependent_data)

        return TrainedSklearnModel(self, trained_regression)
