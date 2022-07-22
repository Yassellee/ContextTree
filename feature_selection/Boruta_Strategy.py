import numpy
from . import config_fs
from boruta import BorutaPy
from sklearn.ensemble import RandomForestClassifier


local_config = config_fs.Config()
local_config.build_data()

class Boruta_Strategy:
    def __init__(self, proessed_data):
        self.data = proessed_data.values
        self.feature_columns = []
        if local_config.if_use_default_label:
            self.labels = numpy.random.randint(10, size=30)
        else:
            self.labels = local_config.labels
        if local_config.if_use_default_feature_columns:
            for i in range(self.data.shape[1]):
                self.feature_columns.append("feature"+str(i))
        else:
            self.feature_columns = local_config.feature_columns

        self.forest = RandomForestClassifier(n_jobs=local_config.n_jobs, class_weight=local_config.class_weight, max_depth=local_config.max_depth)
        self.forest.fit(self.data, self.labels)

    def slimming(self):
        self.feature_selector = BorutaPy(self.forest, n_estimators=local_config.n_estimators, verbose=local_config.verbose, random_state=local_config.random_state)
        self.feature_selector.fit(self.data, self.labels)
        self.processed_data = self.feature_selector.transform(self.data)
    
    def show_feature_names(self):
        self.new_feature_names = self.feature_selector.support_
        
    def standardization(self):
        pass
