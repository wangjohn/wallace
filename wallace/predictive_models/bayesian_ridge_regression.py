from sklearn import linear_model
from wallace.predictive_models.sklearn_model import SklearnModel, TrainedSklearnModel
from wallace.parameters import ParametersGeneralValidityCheck

class BayesianRidgeRegression(SklearnModel):
    def train(self, dataset):
        model = linear_model.BayesianRidge(
                n_iter=self.get_number_iterations(),
                alpha_1=self.get_alpha_1(),
                alpha_2=self.get_alpha_2(),
                lambda_1=self.get_lambda_1(),
                lambda_2=self.get_lambda_2()
                )
        independent_data = self.get_independent_variable_data(dataset)
        dependent_data = self.get_dependent_variable_data(dataset)
        trained_regression = model.fit(independent_data, dependent_data)

        return TrainedSklearnModel(self, trained_regression)

    @classmethod
    def validity_check(klass):
        validity_check = ParametersGeneralValidityCheck()
        validity_check.set_range_parameter("bayesian_ridge_regression.alpha_1", 0.0, 0.001)
        validity_check.set_range_parameter("bayesian_ridge_regression.alpha_2", 0.0, 0.001)
        validity_check.set_range_parameter("bayesian_ridge_regression.lambda_1", 0.0, 0.001)
        validity_check.set_range_parameter("bayesian_ridge_regression.lambda_2", 0.0, 0.001)
        return validity_check

    def get_alpha_1(self):
        return self.parameter_set.get("bayesian_ridge_regression.alpha_1")

    def get_alpha_2(self):
        return self.parameter_set.get("bayesian_ridge_regression.alpha_2")

    def get_lambda_1(self):
        return self.parameter_set.get("bayesian_ridge_regression.lambda_1")

    def get_lambda_2(self):
        return self.parameter_set.get("bayesian_ridge_regression.lambda_2")
