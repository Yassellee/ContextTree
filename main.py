from data_preprocessing.processor import data_frame_builder
from dimension_reduction.PCA_strategy import PCA_strategy
from feature_selection.KBest_Strategy import KBest_Strategy
from decision_tree.tree_builder import Decision_Tree
import config

local_config = config.Config()


def main():
    preprocessed_data = data_frame_builder()

    data_slimming_strategy = None

    if local_config.data_slimming_strategy == "KBest":
        data_slimming_strategy = KBest_Strategy(preprocessed_data)
    elif local_config.data_slimming_strategy == "PCA":
        data_slimming_strategy = PCA_strategy(preprocessed_data)

    data_slimming_strategy.standardization()
    data_slimming_strategy.slimming()

    if local_config.data_slimming_strategy == "KBest":
        data_slimming_strategy.show_feature_names()
        feature_names = data_slimming_strategy.new_feature_names
    elif local_config.data_slimming_strategy == "PCA":
        feature_names = data_slimming_strategy.feature_columns

    decision_tree = Decision_Tree(data_slimming_strategy.processed_data, data_slimming_strategy.labels, feature_names)
    decision_tree.train()
    decision_tree.visualize()

if __name__ == '__main__':
    main()