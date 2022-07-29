from data_preprocessing.processor import data_frame_builder
from dimension_reduction.PCA_strategy import PCA_strategy
from feature_selection.KBest_Strategy import KBest_Strategy
from feature_selection.Boruta_Strategy import Boruta_Strategy
from decision_tree.tree_builder import Decision_Tree
from decision_tree.code_builder import tree_to_code
from decision_tree.rule_builder import get_rules
import config
import codecs

local_config = config.Config()

def build_data():
    return data_frame_builder()


def build_data_slimming_strategy(preprocessed_data):
    if local_config.data_slimming_strategy == "KBest":
        strategy = KBest_Strategy(preprocessed_data)
        strategy.standardization()
        strategy.slimming()
        return strategy
    elif local_config.data_slimming_strategy == "PCA":
        strategy = PCA_strategy(preprocessed_data)
        strategy.standardization()
        strategy.slimming()
        return strategy
    elif local_config.data_slimming_strategy == "Boruta":
        strategy = Boruta_Strategy(preprocessed_data)
        strategy.standardization()
        strategy.slimming()
        return strategy


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


def build_code(decision_tree, feature_names):
    tree_to_code(decision_tree, feature_names)


def build_rule(decision_tree, feature_names, target_names):
    rules = get_rules(decision_tree, feature_names, target_names)
    with codecs.open("rules_in_natural_language.txt", 'w', encoding="UTF-8") as file:
        for r in rules:
            file.writelines(r)
            file.writelines('\r\n')
            file.writelines('\r\n')


def main():
    preprocessed_data = build_data()

    data_slimming_strategy = build_data_slimming_strategy(preprocessed_data)

    feature_names = build_feature_names(data_slimming_strategy)

    decision_tree = build_tree(data_slimming_strategy, feature_names)

    build_code(decision_tree.decision_tree, feature_names)

    build_rule(decision_tree.decision_tree, feature_names, data_slimming_strategy.labels)

if __name__ == '__main__':
    main()