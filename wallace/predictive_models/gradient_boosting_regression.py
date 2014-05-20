from sklearn import ensemble
from wallace.predictive_models.sklearn_model import SklearnModel, TrainedSklearnModel
from wallace.parameters import ParametersGeneralValidityCheck

class GradientBoostingRegression(SklearnModel):
    def train(self, dataset):
        model = ensemble.GradientBoostingRegressor(learning_rate=self.get_learning_rate(), \
                n_estimators=self.get_number_estimators(), \
                max_depth=self.get_max_depth()
                )
        independent_data = self.get_independent_variable_data(dataset)
        dependent_data = self.get_dependent_variable_data(dataset)
        trained_regression = model.fit(independent_data, dependent_data)

        return TrainedSklearnModel(self, trained_regression)

    @classmethod
    def validity_check(klass):
        validity_check = ParametersGeneralValidityCheck()
        validity_check.set_range_parameter("gradient_boosting_regression.learning_rate", 0.0, 1.0)
        validity_check.set_integer_range_parameter("gradient_boosting_regression.number_estimators", 1, 1000)
        validity_check.set_integer_range_parameter("gradient_boosting_regression.max_depth", 1, 100)
        return validity_check

    def get_number_estimators(self):
        return self.parameter_set.get("gradient_boosting_regression.number_estimators")

    def get_learning_rate(self):
        return self.parameter_set.get("gradient_boosting_regression.learning_rate")

    def get_max_depth(self):
        return self.parameter_set.get("gradient_boosting_regression.max_depth")

