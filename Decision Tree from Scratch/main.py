# Decision Tree from Scratch
import pandas as pd


class Node:

  def __init__(self):
    # class initialization
    self.left = None
    self.right = None
    self.term = False
    self.label = None
    self.feature = None
    self.value = None

  def set_split(self, feature, value):
    # this function saves the node splitting feature and its value
    self.feature = feature
    self.value = value

  def set_term(self, label):
    # if the node is a leaf, this function saves its label
    self.term = True
    self.label = label


def gini(labels) -> float:
    probabilities = [label_count / len(labels) for label_count in labels.value_counts()]
    return 1 - sum([prob ** 2 for prob in probabilities])


def weighted_gini(left, right) -> float:
    n = len(left) + len(right)
    return len(left) / n * gini(left) + len(right) / n * gini(right)


def split(data: pd.DataFrame, labels: pd.Series):
    result = []
    for col in data.columns:
        for val in data[col].unique():
            aa = weighted_gini(labels[data[col] == val], labels[data[col] != val])
            result.append((aa, col, val))
    gini_value, col, val = min(result, key=lambda x: x[0])
    return (round(gini_value, 4), col, val,
            data[data[col] == val].index.to_list(), data[data[col] != val].index.to_list())


def split_data(node: Node, data: pd.DataFrame, labels: pd.Series) -> None:
    if is_leaf(data, labels):
        node.set_term(labels[0])
    else:
        _, feature, value, left, right = split(data, labels)
        print(f'Made split: {feature} is {value}')
        node.feature = feature
        node.value = value
        node.left = Node()
        split_data(node.left, data.iloc[left].reset_index(drop=True),
                   labels.iloc[left].reset_index(drop=True))
        node.right = Node()
        split_data(node.right, data.iloc[right].reset_index(drop=True),
                   labels.iloc[right].reset_index(drop=True))


def is_leaf(data, labels):
    if len(data) == 1:
        return True
    if gini(labels) == 0:
        return True
    if max([data[col].nunique() for col in data.columns]) == 1:
        return True


def gini_test():
    node = input().split()
    left_split = input().split()
    right_split = input().split()

    # data = [1, 0, 1, 1, 0, 1, 0, 1, 0]
    # left_split = [1, 0, 1, 1]
    # right_split = [0, 1, 0, 1, 0]

    print(round(gini(node), 2))
    print(round(weighted_gini(pd.Series(left_split), pd.Series(right_split)), 2))


def main() -> None:
    # file_path = '../data/data_stage3.csv'

    file_path = input()
    df = pd.read_csv(file_path, index_col=0)
    X, y = df.iloc[:, :-1], df.iloc[:, -1]

    root = Node()
    split_data(root, X, y)


if __name__ == '__main__':
    main()