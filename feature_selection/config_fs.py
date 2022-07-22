class Config:
    def __init__(self):
        self.feature_columns = []
        self.if_use_default_feature_columns = True
        self.labels = []
        self.if_use_default_label = True
        self.k = 20

        self.n_jobs = -1
        self.class_weight = 'balanced'
        self.max_depth = 5
        self.n_estimators = 'auto'
        self.verbose = 2
        self.random_state = 1
    
    def build_data(self):
        pass