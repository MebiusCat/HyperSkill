# Decision Tree from Scratch

def gini(labels: list[str]) -> float:
    probabilities = [labels.count(label) / len(labels) for label in set(labels)]
    return 1 - sum([prob ** 2 for prob in probabilities])

def weighted_gini(left: list[str], right: list[str]) -> float:
    n = len(left) + len(right)
    return len(left) / n * gini(left) + len(right) / n * gini(right)

def main() -> None:
    node = input().split()
    left_split = input().split()
    right_split = input().split()

    # data = [1, 0, 1, 1, 0, 1, 0, 1, 0]
    # left_split = [1, 0, 1, 1]
    # right_split = [0, 1, 0, 1, 0]

    print(round(gini(node), 2))
    print(round(weighted_gini(left_split, right_split), 2))


if __name__ == '__main__':
    main()