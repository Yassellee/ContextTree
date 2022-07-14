from . import config_dt
import numpy
from sklearn.tree import DecisionTreeClassifier
from matplotlib import pyplot as plt
from sklearn import tree

local_config = config_dt.Config()

class Decision_Tree:
    def __init__(self, preprocessed_data):
        self.data = preprocessed_data
        if local_config.if_use_default_label:
            self.labels = numpy.random.randint(10, size=30)
        else:
            self.labels = local_config.labels
        
    def train(self):
        self.decision_tree = DecisionTreeClassifier()
        self.decision_tree.fit(self.data, self.labels)

    def visualize(self):
        self.feature_columns = []
        if local_config.if_use_default_feature_columns:
            for i in range(self.data.shape[1]):
                self.feature_columns.append("PC"+str(i))
        else:
            self.feature_columns = local_config.feature_columns

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
