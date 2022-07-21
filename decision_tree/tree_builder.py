from . import config_dt
import numpy
from sklearn.tree import DecisionTreeClassifier
from matplotlib import pyplot as plt
from sklearn import tree

local_config = config_dt.Config()
local_config.build_data()

class Decision_Tree:
    def __init__(self, preprocessed_data, labels, feature_columns):
        self.labels = labels
        self.data = preprocessed_data
        self.feature_columns = feature_columns
        
    def train(self):
        self.decision_tree = DecisionTreeClassifier()
        self.decision_tree.fit(self.data, self.labels)

    def visualize(self):
        fig = plt.figure(figsize=(25,20))
        _ = tree.plot_tree(self.decision_tree, 
                   feature_names=self.feature_columns,  
                   class_names=local_config.class_names,
                   filled=True)
        fig.savefig("tree.png")

    def evaluate(self):
        pass

    def predict(self, data_to_predict):
        return self.decision_tree.predict(data_to_predict)
