from wallace.dataset import DatasetVariable

class DatasetTransformation(object):
    def __init__(self, settings):
        self.settings = settings

    def transform(self, dataset, variables=None):
        if variables == None:
            variables = [DatasetVariable(i) for i in xrange(dataset.num_cols)]

        filtered_matrix = dataset.get_filtered_matrix(variables)
        raise NotImplementedError()

    def transform_column(self, column):
        raise NotImplementedError()
