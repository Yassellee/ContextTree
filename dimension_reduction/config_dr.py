class Config:
    def __init__(self):
        self.feature_columns = []
        self.if_use_default_feature_columns = True
        self.labels = []
        self.if_use_default_label = True
        self.n_components = 0.90
        self.random_state = 2022
    
    def build_data(self):
        pass