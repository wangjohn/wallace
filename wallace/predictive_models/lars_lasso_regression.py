from sklearn import linear_model
from wallace.predictive_models.sklearn_model import SklearnModel, TrainedSklearnModel
from wallace.parameters import ParametersGeneralValidityCheck

class LarsLassoRegression(SklearnModel):
    def train(self, dataset):
        model = linear_model.LassoLars(alpha=self.get_alpha())
        independent_data = self.get_independent_variable_data(dataset)
        dependent_data = self.get_dependent_variable_data(dataset)
        trained_regression = model.fit(independent_data, dependent_data)

        return TrainedSklearnModel(self, trained_regression)

    @classmethod
    def validity_check(klass):
        validity_check = ParametersGeneralValidityCheck()
        validity_check.set_range_parameter("lars_lasso_regression.alpha", 0.0, 1.0)
        return validity_check

    def get_alpha(self):
        return self.parameter_set.get("lars_lasso_regression.alpha")
