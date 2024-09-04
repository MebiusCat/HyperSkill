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


class DecisionTree:

    def __init__(self, root, min_samples=1, log_fit=False, log_predict=False):
        self.root = root
        self.min_samples = min_samples
        self.log_train = log_fit
        self.log_predict = log_predict

    def fit(self, X, y):
        self.split_data(self.root, X, y)

    def predict(self, X_test):
        y_test = []
        for idx, row in X_test.iterrows():
            if self.log_predict:
                print(f'Prediction for sample # {idx}')
            y_test.append(self.predict_label(self.root, row))

    def predict_label(self, node: Node, obs):
        if node.term:
            if self.log_predict:
                print(f'\tPredicted label: {node.label}')
            return node.label
        else:
            if self.log_predict:
                print(f'\tConsidering decision rule on feature {node.feature} with value {node.value}')

            side = node.left if obs[node.feature] == node.value else node.right
            return self.predict_label(side, obs)

    @staticmethod
    def _gini(labels) -> float:
        probabilities = [label_count / len(labels) for label_count in labels.value_counts()]
        return 1 - sum([prob ** 2 for prob in probabilities])

    @staticmethod
    def _weighted_gini(left, right) -> float:
        n = len(left) + len(right)
        return len(left) / n * DecisionTree._gini(left) + len(right) / n * DecisionTree._gini(right)

    def split(self, data: pd.DataFrame, labels: pd.Series):
        result = []
        for col in data.columns:
            for val in data[col].unique():
                weight = DecisionTree._weighted_gini(labels[data[col] == val], labels[data[col] != val])
                result.append((weight, col, val))
        gini_value, col, val = min(result, key=lambda x: x[0])
        return (round(gini_value, 4), col, val,
                data[data[col] == val].index.to_list(), data[data[col] != val].index.to_list())

    def split_data(self, node: Node, data: pd.DataFrame, labels: pd.Series) -> None:
        if DecisionTree.is_leaf(data, labels):
            node.set_term(labels[0])
        else:
            _, feature, value, left, right = self.split(data, labels)
            if self.log_train:
                print(f'Made split: {feature} is {value}')
            node.feature = feature
            node.value = value
            node.left = Node()
            self.split_data(node.left, data.iloc[left].reset_index(drop=True),
                            labels.iloc[left].reset_index(drop=True))
            node.right = Node()
            self.split_data(node.right, data.iloc[right].reset_index(drop=True),
                            labels.iloc[right].reset_index(drop=True))

    @staticmethod
    def is_leaf(data, labels):
        if len(data) == 1:
            return True
        if DecisionTree._gini(labels) == 0:
            return True
        if max([data[col].nunique() for col in data.columns]) == 1:
            return True

    @staticmethod
    def gini_test():
        node = input().split()
        left_split = input().split()
        right_split = input().split()

        # data = [1, 0, 1, 1, 0, 1, 0, 1, 0]
        # left_split = [1, 0, 1, 1]
        # right_split = [0, 1, 0, 1, 0]

        print(round(DecisionTree._gini(node), 2))
        print(round(DecisionTree._weighted_gini(pd.Series(left_split), pd.Series(right_split)), 2))


def main() -> None:
    # file_path_train = '../data/data_stage5_train.csv'
    # file_path_test = '../data/data_stage5_test.csv'

    file_path_train, file_path_test = input().split()

    df = pd.read_csv(file_path_train, index_col=0)
    X, y = df.iloc[:, :-1], df.iloc[:, -1]
    tree = DecisionTree(Node(), log_predict=True)
    tree.fit(X, y)

    df_test = pd.read_csv(file_path_test, index_col=0)
    tree.predict(df_test)


if __name__ == '__main__':
    main()