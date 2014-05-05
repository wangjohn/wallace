from sklearn import linear_model
from wallace.predictive_models.predictive_model import PredictiveModel, TrainedSklearnModel
from wallace.parameters import ParametersGeneralValidityCheck

class RidgeRegression(PredictiveModel):
    def train(self, dataset):
        model = linear_model.Ridge(alpha=self.get_alpha())
        independent_data = self.get_independent_variable_data(dataset)
        dependent_data = self.get_dependent_variable_data(dataset)
        trained_regression = model.fit(independent_data, dependent_data)

        return TrainedSklearnModel(self, trained_regression)

    @classmethod
    def required_parameters(klass):
        return ["ridge_regression_alpha"]

    @classmethod
    def validity_check(klass):
        validity_check = ParametersGeneralValidityCheck()
        validity_check.set_range_parameter("ridge_regression_alpha", 0.0, 1.0)
        return validity_check

    def get_alpha(self):
        return self.parameter_set.get("ridge_regression_alpha")
