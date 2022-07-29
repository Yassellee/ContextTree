from data_preprocessing.processor import data_frame_builder
from dimension_reduction.PCA_strategy import PCA_strategy
from feature_selection.KBest_Strategy import KBest_Strategy
from feature_selection.Boruta_Strategy import Boruta_Strategy
from decision_tree.tree_builder import Decision_Tree
import config

local_config = config.Config()

def build_data():
    return data_frame_builder()


def build_data_slimming_strategy(preprocessed_data):
    if local_config.data_slimming_strategy == "KBest":
        return KBest_Strategy(preprocessed_data).standardization().slimming()
    elif local_config.data_slimming_strategy == "PCA":
        return PCA_strategy(preprocessed_data).standardization().slimming()
    elif local_config.data_slimming_strategy == "Boruta":
        return Boruta_Strategy(preprocessed_data).standardization().slimming()


def build_feature_names(data_slimming_strategy):
    if local_config.data_slimming_strategy == "KBest":
        data_slimming_strategy.show_feature_names()
        return data_slimming_strategy.new_feature_names
    elif local_config.data_slimming_strategy == "PCA":
        return data_slimming_strategy.feature_columns
    elif local_config.data_slimming_strategy == "Boruta":
        data_slimming_strategy.show_feature_names()
        return data_slimming_strategy.new_feature_names


def build_tree(data_slimming_strategy, feature_names):
    decision_tree = Decision_Tree(data_slimming_strategy.processed_data, data_slimming_strategy.labels, feature_names)
    decision_tree.train()
    decision_tree.visualize()
    return decision_tree


def main():
    preprocessed_data = build_data()

    data_slimming_strategy = build_data_slimming_strategy(preprocessed_data)

    feature_names = build_feature_names(data_slimming_strategy)

    decision_tree = build_tree(data_slimming_strategy, feature_names)

if __name__ == '__main__':
    main()