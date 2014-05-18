from sklearn import svm
from wallace.predictive_models.sklearn_model import SklearnModel, TrainedSklearnModel
from wallace.parameters import ParametersGeneralValidityCheck

class SvmSvcRegression(SklearnModel):
    def train(self, dataset):
        model = svm.SVC(
                penalty_parmeter=self.get_penalty_parameter(),
                kernel=self.get_kernel(),
                shrinking=self.get_shrinking(),
                )
        independent_data = self.get_independent_variable_data(dataset)
        dependent_data = self.get_dependent_variable_data(dataset)
        trained_regression = model.fit(independent_data, dependent_data)

        return TrainedSklearnModel(self, trained_regression)

    @classmethod
    def validity_check(klass):
        validity_check = ParametersGeneralValidityCheck()
        validity_check.set_range_parameter("svm_svc_regression.penalty_parameter", 0.0, 5.0)
        validity_check.set_category_parameter("svm_svc_regression.kernel",
            ["linear", "poly", "rbf", "sigmoid", "precomputed"])
        validity_check.set_category_parameter("svm_svc_regression.shrinking", [True, False])
        return validity_check

    def get_penalty_parameter(self):
        return self.parameter_set.get("svm_svc_regression.penalty_parameter")

    def get_kernel(self):
        return self.parameter_set.get("svm_svc_regression.kernel")

    def get_shrinking(self):
        return self.parameter_set.get("svm_svc_regression.shrinking")
