from . import config_dr
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy


local_config = config_dr.Config()

class PCA_strategy:
    def __init__(self, proessed_data):
        self.data = proessed_data.values
    
    def standardization(self):
        scaler = StandardScaler()
        scaler.fit(self.data)
        self.scaled_data = scaler.transform(self.data)

    def dimension_reduction(self):
        self.processed_data_with_info = PCA(n_components=local_config.n_components, 
                                  random_state=local_config.random_state)
        self.processed_data_with_info.fit(self.scaled_data)
        self.processed_data = self.processed_data_with_info.transform(self.scaled_data)
    
    def check_explained_variance_ratio(self, n):
        n = min(n, self.processed_data.shape[1]-1)
        return numpy.cumsum(self.processed_data_with_info.explained_variance_ratio_*100)[n]

    def check_dimension(self):
        return self.processed_data.shape[1]


