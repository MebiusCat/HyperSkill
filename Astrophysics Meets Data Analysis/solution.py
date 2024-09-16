# Per aspera ad astra

from scipy.stats import shapiro, fligner, f_oneway

import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('../Data/groups.tsv', delimiter='\t')

df = df.dropna()
# print(df.head())
data = [df[df.features == feature].mean_mu for feature in [1, 0]]
# means = (df.groupby('features')
#          .agg({'mean_mu': 'mean'})
#          .sort_values('features', ascending=False)
#          .mean_mu
#          .round(5)
#          .to_list())
#
# fig, ax = plt.subplots(figsize=(12, 8))
#
# for i, mean in enumerate(means):
#     ax.text(i + 1, mean, f'{mean:.2f}', horizontalalignment='center')
#
# plt.boxplot(data, tick_labels=[1, 0], showmeans=True)
# ax.invert_yaxis()
# plt.show()

# print(*means)

# looks like normal
test_shapiro = [shapiro(df[df.features == feature].mean_mu)[1] for feature in [1, 0]]
print(*test_shapiro, end=' ')

# the smaller statistic the smaller difference between variance
print(fligner(*data)[1], end=' ')

# one-way analysis of variance (ANOVA)
F, p = f_oneway(data[0], data[1])
print(p)
