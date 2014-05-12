from wallace.dataset import DatasetVariable
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
            variables = [DatasetVariable(i) for i in xrange(len(dataset.num_cols))]

        resulting_datasets = [dataset]
        for transformation in self.transformations:
            current_dataset = transformation.transform(dataset, variables)
            resulting_datasets.append(current_dataset)

        return Dataset.merge_datasets(resulting_datasets)

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
