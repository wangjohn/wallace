from wallace.dataset import Dataset, DatasetVariable
from wallace.dataset_transformations.dataset_transformation import DatasetTransformation

class DatasetTransformer(object):
    def __init__(self, settings, transformations=None):
        self.settings = settings
        self.transformations = self._initialize_transformations(transformations)

    def add_transformation(self, transformation):
        transformation = self._cast_transformation(transformation)
        self.transformations.append(transformation)

    def transform(self, dataset, variables=None):
        transformed_columns = []
        transformed_headers = []
        if variables == None:
            variables = [DatasetVariable(i) for i in xrange(dataset.num_cols)]

        resulting_datasets = [dataset]
        for transformation in self.transformations:
            current_dataset = transformation.transform(dataset, variables)
            resulting_datasets.append(current_dataset)

        return self.merge_datasets(resulting_datasets)

    def merge_datasets(self, datasets):
        if len(datasets) < 1:
            raise ValueError("Must specify at least one dataset to merge.")

        first_dataset = datasets[0]
        num_rows = first_dataset.num_rows
        data_matrix = []
        for i in xrange(num_rows):
            data_matrix.append(list(first_dataset.get_row(i)))

        if first_dataset.headers == None:
            headers = None
        else:
            headers = list(first_dataset.headers)

        for dataset in datasets[1:]:
            headers = self._merge_headers(headers, dataset)
            data_matrix = self._merge_data_matrix(data_matrix, dataset, num_rows)
        return Dataset(data_matrix, headers)

    def _merge_headers(self, headers, dataset):
        if (headers == None and dataset.headers != None) or (headers != None and dataset.headers == None):
            raise ValueError("Inconsistent headers when merging datasets. Either all datasets must have headers or none can have headers.")

        if headers != None:
            for header in dataset.headers:
                headers.append(header)
            return headers

    def _merge_data_matrix(self, data_matrix, dataset, num_rows):
        if dataset.num_rows != num_rows:
            raise ValueError("Merging datasets requires that all datasets have the same number of rows.")

        for i in xrange(num_rows):
            data_matrix[i].extend(dataset.get_row(i))
        return data_matrix

    def _initialize_transformations(self, transformations):
        if transformations == None:
            if self.settings.has("dataset_transformation.default_transformations"):
                return self.settings.get("dataset_transformation.default_transformations")
            else:
                return []
        else:
            return [self._cast_transformation(transform) for transform in transformations]

    def _cast_transformation(self, transform):
         if isinstance(transform, DatasetTransformation):
             return transform
         elif issubclass(transform, DatasetTransformation):
             return transform(self.settings)
         else:
             raise ValueError("Transformations must be either an instance or subclass of `DatasetTransformation`.")
