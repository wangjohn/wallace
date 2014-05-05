from sklearn import linear_model
from wallace.predictive_models.predictive_model import PredictiveModel, TrainedSklearnModel

class LassoRegression(PredictiveModel):
    def train(self, dataset):
        model = linear_model.Lasso(alpha=self.get_alpha())
        independent_data = self.get_independent_variable_data(dataset)
        dependent_data = self.get_dependent_variable_data(dataset)
        trained_regression = model.fit(independent_data, dependent_data)

        return TrainedSklearnModel(self, trained_regression)

    @classmethod
    def required_parameters(self):
        return ["lasso_regression_alpha"]

    def get_alpha(self):
        return self.parameter_set.get("lasso_regression_alpha")
