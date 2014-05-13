from collections import defaultdict

class CategoricalVariableEncoder(object):
    def convert_categorical_variables(self, data_matrix, category_indices, category_value_mapping=None):
        if len(category_indices) == 0:
            return data_matrix

        if category_value_mapping == None:
            category_value_mapping = self.get_category_value_mapping(data_matrix, category_indices)

        for i in xrange(len(data_matrix)):
            for category_index in category_indices:
                current_data_value = data_matrix[i][category_index]
                updated_data_value = category_value_mapping[category_index][current_data_value]
                data_matrix[i][category_index] = updated_data_value

        return data_matrix

    def get_category_value_mapping(self, data_matrix, category_indices):
        categories = self.get_category_values(data_matrix, category_indices)

        category_value_mapping = {}
        for category_index, values_set in categories.iteritems():
            category_value_mapping[category_index] = self.create_value_map(values_set)

        return category_value_mapping

    def get_category_values(self, data_matrix, category_indices):
        categories = {}
        for category_index in category_indices:
            categories[category_index] = set()

        for i in xrange(len(data_matrix)):
            for category_index in category_indices:
                category_value = data_matrix[i][category_index]
                categories[category_index].add(category_value)

        return categories

    @classmethod
    def create_value_map(self, values_set):
        sorted_values_set = sorted(values_set)
        value_mapping = {}
        for i in xrange(len(sorted_values_set)):
            value_mapping[sorted_values_set[i]] = i
        return value_mapping
