# Per Aspera ad Astra
from astropy.coordinates import SkyCoord
from astropy.cosmology import FlatLambdaCDM
from astropy import units as u
from itertools import combinations
from scipy.stats import (shapiro,
                         fligner,
                         f_oneway,
                         ks_2samp,
                         pearsonr)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def stage_1():
    df = pd.read_csv('../Data/groups.tsv', delimiter='\t')
    df = df.dropna()

    data = [df[df.features == feature].mean_mu for feature in [1, 0]]

    means = (df.groupby('features')
             .agg({'mean_mu': 'mean'})
             .sort_values('features', ascending=False)
             .mean_mu
             .round(5)
             .to_list())

    fig, ax = plt.subplots(figsize=(12, 8))

    for i, mean in enumerate(means):
        ax.text(i + 1, mean, f'{mean:.2f}', horizontalalignment='center')

    plt.boxplot(data, tick_labels=[1, 0], showmeans=True)
    ax.invert_yaxis()
    plt.show()

    print(*means)


def stage_2():
    df = pd.read_csv('../Data/groups.tsv', delimiter='\t')
    df = df.dropna()

    data = [df[df.features == feature].mean_mu for feature in [1, 0]]

    # looks like normal
    test_shapiro = [shapiro(df[df.features == feature].mean_mu)[1] for feature in [1, 0]]
    print(*test_shapiro, end=' ')

    # the smaller statistic the smaller difference between variance
    print(fligner(*data)[1], end=' ')

    # one-way analysis of variance (ANOVA)
    F, p = f_oneway(data[0], data[1])
    print(p)


def stage_3():
    df_morph = pd.read_csv('../Data/galaxies_morphology.tsv', delimiter='\t')
    df_isol = pd.read_csv('../Data/isolated_galaxies.tsv', delimiter='\t')

    bins = np.arange(0.0, 13.0, 0.5)

    fig, ax = plt.subplots(figsize=(12, 8))
    plt.hist(df_isol.n, bins, edgecolor='black', color='red', label='isolated galaxies', alpha=0.5, hatch='/')
    plt.hist(df_morph.n, bins, edgecolor='black', color='blue', label='groups galaxies', alpha=0.5, hatch='\\')
    plt.xlabel('n')
    plt.ylabel('Count')
    plt.legend(['isolated galaxies', 'groups galaxies'])
    plt.grid()
    plt.show()

    print(f'{(df_morph.n > 2).sum() / df_morph.shape[0]:.5f}', end=' ')
    print(f'{(df_isol.n > 2).sum() / df_isol.shape[0]:.5f}', end=' ')
    print(ks_2samp(df_morph.n, df_isol.n).pvalue)


def stage_4():
    df_morph = pd.read_csv('../Data/galaxies_morphology.tsv', delimiter='\t')
    df_groups = pd.read_csv('../Data/groups.tsv', delimiter='\t').dropna()

    df_mean = df_morph.groupby('Group').agg({'n': 'mean', 'T': 'mean'})
    df_mean.rename(columns={'n': 'mean_n', 'T': 'mean_T'}, inplace=True)
    df_mean = df_mean.merge(df_groups, on='Group')

    plt.scatter(df_mean.mean_mu, df_mean.mean_n)
    # plt.show()

    plt.scatter(df_mean.mean_mu, df_mean.mean_T)
    # plt.show()

    print(f'{shapiro(df_mean.mean_mu).pvalue:.5f}', end=' ')
    print(f'{shapiro(df_mean.mean_n).pvalue:.5f}', end=' ')
    print(f'{shapiro(df_mean.mean_T).pvalue:.5f}', end=' ')

    print(f'{pearsonr(df_mean.mean_mu, df_mean.mean_n).pvalue:.5f}', end=' ')
    print(f'{pearsonr(df_mean.mean_mu, df_mean.mean_T).pvalue}')


def calc_separation(group_df):
    result = []
    galaxies = group_df.iterrows()
    for obj1, obj2 in list(combinations(galaxies, 2)):
        p1 = SkyCoord(ra=obj1[1].RA * u.degree, dec=obj1[1].DEC * u.degree, frame="fk5")
        p2 = SkyCoord(ra=obj2[1].RA * u.degree, dec=obj2[1].DEC * u.degree, frame="fk5")
        result.append(p1.separation(p2).to(u.rad).value)

    return np.median(result)


def stage_5():
    my_cosmo = FlatLambdaCDM(H0=67.74, Om0=0.3089)

    df = pd.read_csv('../Data/galaxies_coordinates.tsv', delimiter='\t', index_col=1)
    df_groups = pd.read_csv('../Data/groups.tsv', delimiter='\t', index_col=0).dropna()

    df_groups['dist'] = df_groups.z.map(lambda x: my_cosmo.angular_diameter_distance(x).to(u.kpc))

    separation = df.groupby('Group', group_keys=False)[['RA', 'DEC', 'Group']].apply(calc_separation)
    df_groups['sep'] = df_groups.index.map(separation) * df_groups['dist']
    df_groups['sep'] = df_groups['sep'].apply(lambda x: x.value)

    plt.scatter(df_groups.sep, df_groups.mean_mu)
    # plt.show()

    print(f'{df_groups.loc["HCG 2"].sep:.6f}', end=' ')
    print(f'{shapiro(df_groups.sep).pvalue:.6f}', end=' ')
    print(f'{shapiro(df_groups.mean_mu).pvalue:.6f}', end=' ')
    print(f'{pearsonr(df_groups.mean_mu, df_groups.sep).pvalue:.6f}')


if __name__ == '__main__':
    stage_5()
