class DatasetCleaner(object):
    def __init__(self, settings, data_matrix):
        self.settings = settings
        self.data_matrix = data_matrix

    def clean(self):
        raise NotImplementedError()

    def clean_row(self, row):
        pass
