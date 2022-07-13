from data_preprocessing.processor import data_frame_builder
from dimension_reduction.PCA_strategy import PCA_strategy
from decision_tree.tree_builder import Decision_Tree


def main():
    pca_class = PCA_strategy(data_frame_builder())
    pca_class.standardization()
    pca_class.dimension_reduction()
    decision_tree = Decision_Tree(pca_class.processed_data)
    decision_tree.train()
    decision_tree.visualize()

if __name__ == '__main__':
    main()