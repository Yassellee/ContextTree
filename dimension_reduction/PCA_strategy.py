from . import config_dr
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy


local_config = config_dr.Config()
local_config.build_data()

class PCA_strategy:
    def __init__(self, proessed_data):
        self.data = proessed_data.values
        self.feature_columns = []
        if local_config.if_use_default_label:
            self.labels = numpy.random.randint(10, size=30)
        else:
            self.labels = local_config.labels
        if local_config.if_use_default_feature_columns:
            for i in range(self.data.shape[1]):
                self.feature_columns.append("PC"+str(i))
        else:
            self.feature_columns = local_config.feature_columns
    
    def standardization(self):
        scaler = StandardScaler()
        scaler.fit(self.data)
        self.scaled_data = scaler.transform(self.data)

    def slimming(self):
        self.processed_data_with_info = PCA(n_components=local_config.n_components, 
                                  random_state=local_config.random_state)
        self.processed_data_with_info.fit(self.scaled_data)
        self.processed_data = self.processed_data_with_info.transform(self.scaled_data)
    
    def check_explained_variance_ratio(self, n):
        n = min(n, self.processed_data.shape[1]-1)
        return numpy.cumsum(self.processed_data_with_info.explained_variance_ratio_*100)[n]

    def check_dimension(self):
        return self.processed_data.shape[1]


