# ContextTree

## 功能简介

> 将手机标注好的手机情景数据进行降维处理后用于建树，通过决策树获得情景推荐规则。



## 代码结构

- data_preprocessing

> 数据预处理。通过修改该目录下的config_preprocessing.py实现数据的个性化。如果不希望提供数据，只是希望用默认数据观看demo的话，保留原始config内容即可；如果希望自定义数据，该config文件中各参数含义如下
>
> - num_context：情景种类个数
>
> - if_use_raw_data：是否使用自定义数据，默认为False，若需自定义数据改为True
>
> - dict_raw_data：自定义数据，为python字典，字典格式如下：
>
>   ```python
>   {
>   "<情景名>": [<一个列表，每个列表项代表该情景下对应样本的数据>],
>   "context0": [1, 2, 4, 8, 4, 6, 9, 1.2, -4]
>   }
>   ```
>
> 当if_use_raw_data为False时，执行default_data_builder；否则执行custom_data_builder

- dimension_reduction

> 数据降维。通过修改config_dr.py中参数实现调参。其中，
>
> - n_components：保留信息量阈值。为正整数时，代表最终保留的情景种类（Principal Component数量）数量，按照信息量从大到小保留；为0-1之间的浮点数时，代表保留的信息量阈值，如0.9代表最终保留的Principal Component数量可以保留90%的原始信息量。
> - random_state：随机数种子。
>
> PCA_strategy类中，
>
> - 构造函数传入data_preprocessing部分的返回值进行初始化。
> - standardization对数据进行单位化。
> - dimension_reduction执行降维处理。
> - check_explained_variance_ratio传入正整数n。检查前n个Principal Components保留的信息量。
> - check_dimension。检查降维后的信息维度。

- decision_tree

> 决策树的训练，验证和预测。通过修改config_dt.py中参数实现调参。其中，
>
> - labels：列表，列表项为按顺序排列的样本分类标签。
> - if_use_default_label：布尔值，默认为True。为True时，使用默认的随机生成的标签，用于demo；为False时，使用self.labels中标签。
> - feature_columns：列表，列表项为按顺序排列的情景名。
> - if_use_default_feature_columns：布尔值，默认为True。为True时，使用默认的生成的情景名，用于demo；为False时，使用self.feature_columns。
> - class_names：所有分类结果的名称的列表。
>
> Decision_Tree类中，
>
> - 构造函数传入PCA_strategy中的processed_data进行初始化。
> - train进行训练。
> - visualize进行可视化。
> - evaluate在验证集上测试各项指标。（待实现）
> - predict预测。



## 目前实现

- 数据降维策略为PCA。
- 分类策略为决策树。



## 待实现

- 测试多种数据降维策略。
- 规定情景信息格式。
- 实现决策树验证方法用于测试。