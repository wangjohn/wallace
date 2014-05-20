from sklearn import ensemble
from wallace.predictive_models.sklearn_model import SklearnModel, TrainedSklearnModel
from wallace.parameters import ParametersGeneralValidityCheck

class RandomForestRegression(SklearnModel):
    def train(self, dataset):
        model = ensemble.RandomForestRegressor(n_estimators=self.get_number_estimators())
        independent_data = self.get_independent_variable_data(dataset)
        dependent_data = self.get_dependent_variable_data(dataset)
        trained_regression = model.fit(independent_data, dependent_data)

        return TrainedSklearnModel(self, trained_regression)

    @classmethod
    def validity_check(klass):
        validity_check = ParametersGeneralValidityCheck()
        validity_check.set_integer_range_parameter("random_forest_regression.number_estimators", 1, 100)
        return validity_check

    def get_number_estimators(self):
        return self.parameter_set.get("random_forest_regression.number_estimators")
