from sklearn.feature_selection import SelectKBest, chi2
import numpy
from . import config_fs


local_config = config_fs.Config()
local_config.build_data()

class KBest_Strategy:
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

    def slimming(self):
        self.processed_data_info = SelectKBest(chi2, k=local_config.k)
        self.processed_data = self.processed_data_info.fit_transform(X=self.data, y=self.labels)
    
    def show_feature_names(self):
        self.new_feature_names = self.processed_data_info.get_feature_names_out(self.feature_columns)

    def standardization(self):
        pass
