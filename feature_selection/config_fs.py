class Config:
    def __init__(self):
        self.feature_columns = []
        self.if_use_default_feature_columns = True
        self.labels = []
        self.if_use_default_label = True
        self.k = 20
    
    def build_data(self):
        pass