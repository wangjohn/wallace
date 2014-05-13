from sklearn import preprocessing

from wallace.predictive_models.predictive_model import PredictiveModel, TrainedPredictiveModel
from wallace.categorical_variable_encoder import CategoricalVariableEncoder

class SklearnModel(PredictiveModel):
    def get_dependent_variable_data(self, dataset):
        return dataset.get_filtered_column(self.dependent_variable)

    def get_independent_variable_data(self, dataset):
        filtered_matrix = dataset.get_filtered_matrix(self.independent_variables)
        filtered_data_types = dataset.get_filtered_data_types(self.independent_variables)
        categorical_features, category_value_mapping = self.get_categorical_features(filtered_data_types)

        variable_encoder = CategoricalVariableEncoder()
        filtered_matrix = variable_encoder.convert_categorical_variables(filtered_matrix, categorical_features, category_value_mapping)

        encoder = preprocessing.OneHotEncoder(categorical_features=categorical_features)
        data_result = encoder.fit_transform(filtered_matrix)

        # Take care of sparse and non-sparse matrices. If we have any categorical
        # variables, then it is likely we will get back a sparse matrix and will
        # need to convert it into an array.
        try:
            return data_result.toarray()
        except AttributeError:
            return data_result

    def get_categorical_features(self, filtered_data_types):
        categorical_features = []
        category_value_mapping = {}
        for i in xrange(len(filtered_data_types)):
            data_type = filtered_data_types[i]
            if data_type.is_equal("string") or data_type.is_equal("boolean"):
                categorical_features.append(i)
                category_value_mapping[i] = CategoricalVariableEncoder.create_value_map(data_type.categories)
        return categorical_features, category_value_mapping

class TrainedSklearnModel(TrainedPredictiveModel):
    def __init__(self, predictive_model, fitted_regression):
        TrainedPredictiveModel.__init__(self, predictive_model)
        self.fitted_regression = fitted_regression

    def predict(self, dataset):
        independent_data = self.predictive_model.get_independent_variable_data(dataset)
        return self.fitted_regression.predict(independent_data)
