# Decision Tree from Scratch
import pandas as pd


def gini(labels: list[str]) -> float:
    probabilities = [label_count / len(labels) for label_count in labels.value_counts()]
    return 1 - sum([prob ** 2 for prob in probabilities])


def weighted_gini(left: list[str], right: list[str]) -> float:
    n = len(left) + len(right)
    return len(left) / n * gini(left) + len(right) / n * gini(right)


def split(data, labels):
    result = []
    for col in data.columns:
        for val in data[col].unique():
            aa = weighted_gini(labels[data[col] == val], labels[data[col] != val])
            result.append((aa, col, val))
    gini_value, col, val = min(result, key=lambda x: x[0])
    print(round(gini_value, 4), col, val,
          data[data[col] == val].index.to_list(), data[data[col] != val].index.to_list())


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
    # file_path = '../data/data_stage2.csv'
    file_path = input()
    df = pd.read_csv(file_path, index_col=0)
    X, y = df.iloc[:, :-1], df.iloc[:, -1]
    split(X, y)


if __name__ == '__main__':
    main()