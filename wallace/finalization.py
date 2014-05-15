from datetime import datetime

class WallaceFinalization(object):
    def __init__(self, settings, model_tracking):
        self.settings = settings
        self.model_tracking = model_tracking

    def print_results(self, filename=None):
        if filename == None:
            filename = self.settings.get("model_tracking.results_file")

        with open(filename, "a+") as f:
            f.write("Wallace Optimization Results - ")
            f.write(datetime.now().isoformat())
            f.write("\n\n")
            f.write("Dataset Source: '%s'" % self.settings.)

class FinalizationLogging(object):

    def __init__(self, settings, dependent_variable, dataset_filename):
        self.settings = settings
        self.dependent_variable = dependent_variable
        self.dataset_filename = dataset_filename

    def header(self):
        return "Wallace Optimization Results - %s\n\n" % datetime.now().isoformat()

    def dataset_source(self):
        return "Dataset Source: '%s'\n" % self.dataset_filename

    def settings(self):
        pass

    def best_models(self, model_tracking, number=1):
        best_models = model_tracking.best_models()[:number]
        descriptions = []
        for i in xrange(len(best_models)):
            model, fitness = best_models[i]

            model_description = ("Model Rank: %s\n" % (i+1)
                    "Model Fitness: %s\n" % fitness
                    "Model Name: %s\n" % model.model_name()
                    "Model Dependent Variable: %s\n" % model.dependent_variable.variable
                    "Model Independent Variables: %s\n" % ", ".join([var.variable for var in model.independent_variables])
                    "Model Parameters: %s\n" % model.get_parameters())
            descriptions.append(model_description)

        return "\n".join(descriptions)
