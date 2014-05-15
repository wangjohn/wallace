from datetime import datetime

class ResultsLogger(object):
    def __init__(self, settings, dataset_filename, model_tracking):
        self.settings = settings
        self.dataset_filename = dataset_filename
        self.model_tracking = model_tracking

    def write_results(self, results_filename=None):
        message_list = [
                self.header() + "\n\n",
                self.dataset_source(),
                self.best_models(),
                self.settings()
                ]
        message = "\n".join(message_list)

        if results_filename == None:
            results_filename = self.settings.get("optimization_algorithm_tracking.final_results_filename")

        with open(results_filename, 'w+') as f:
            f.write(message)

    def header(self):
        return "Wallace Optimization Results - %s\n" % datetime.now().isoformat()

    def dataset_source(self):
        return "Dataset Source: '%s'" % self.dataset_filename

    def settings(self):
        setting_strings = []
        for setting_name, value in self.settings.iteritems():
            setting_strings.append("%s: %s" % (setting_name, value))
        return "\n".join(setting_strings)

    def best_models(self, number=1):
        best_models = self.model_tracking.best_models()[:number]
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
