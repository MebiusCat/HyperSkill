# Per Aspera ad Astra
from astropy.coordinates import SkyCoord
from astropy.cosmology import FlatLambdaCDM
from astropy import units as u
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st

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
    test_shapiro = [st.shapiro(df[df.features == feature].mean_mu)[1] for feature in [1, 0]]
    print(*test_shapiro, end=' ')

    # the smaller statistic the smaller difference between variance
    print(st.fligner(*data)[1], end=' ')

    # one-way analysis of variance (ANOVA)
    F, p = st.f_oneway(data[0], data[1])
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
    print(st.ks_2samp(df_morph.n, df_isol.n).pvalue)


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

    shapiro_pvalue_mu = st.shapiro(
        df_mean.mean_mu
    ).pvalue

    shapiro_pvalue_n = st.shapiro(
        df_mean.mean_n
    ).pvalue

    shapiro_pvalue_T = st.shapiro(
        df_mean.mean_T
    ).pvalue

    pearson_pvalue_mu_n = st.pearsonr(
        df_mean.mean_mu,
        df_mean.mean_n
    ).pvalue

    pearson_pvalue_mu_T = st.pearsonr(
        df_mean.mean_mu,
        df_mean.mean_T
    ).pvalue

    print('{:.5f} {:.5f} {:.5f} {:.5f} {:.5f}'.format(
        shapiro_pvalue_mu,
        shapiro_pvalue_n,
        shapiro_pvalue_T,
        pearson_pvalue_mu_n,
        pearson_pvalue_mu_T
    ))


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

    separation_hcg_2 = df_groups.loc["HCG 2"].sep
    shapiro_pvalue_separation = st.shapiro(
        df_groups.sep
    ).pvalue

    shapiro_pvalue_mu = st.shapiro(
        df_groups.mean_mu
    ).pvalue

    pearson_pvalue = st.pearsonr(
        df_groups.mean_mu,
        df_groups.sep
    ).pvalue

    print('{:.6f} {:.6f} {:.6f} {:.6f}'.format(
        separation_hcg_2,
        shapiro_pvalue_separation,
        shapiro_pvalue_mu,
        pearson_pvalue
    ))


if __name__ == '__main__':
    stage_5()
