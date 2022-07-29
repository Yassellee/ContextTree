from sklearn.tree import _tree
import numpy as np
import codecs

def tree_to_code(tree, feature_names):
    with codecs.open(".\\rules_in_python.py", "w", encoding="UTF-8") as file:
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        # feature_names = [f.replace(" ", "_")[:-5] for f in feature_names]
        file.writelines("def predict({}):".format(", ".join(feature_names)))
        file.writelines('\n')

        def recurse(node, depth):
            indent = "    " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                file.writelines("{}if {} <= {}:".format(indent, name, np.round(threshold,2)))
                file.writelines('\n')
                recurse(tree_.children_left[node], depth + 1)
                file.writelines("{}else:  # if {} > {}".format(indent, name, np.round(threshold,2)))
                file.writelines('\n')
                recurse(tree_.children_right[node], depth + 1)
            else:
                file.writelines("{}return \"{}\"".format(indent, tree_.value[node]))
                file.writelines('\n')

        recurse(0, 1)