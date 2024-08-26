import numpy as np
import pandas as pd

np.random.seed(30)

if __name__ == '__main__':
    pd.set_option('display.max_columns', 8)

    df_general = pd.read_csv('test/general.csv')
    df_prenatal = pd.read_csv('test/prenatal.csv')
    df_sport = pd.read_csv('test/sports.csv')

    # Stage 1
    # print(df_general.head(20))
    # print(df_prenatal.head(20))
    # print(df_sport.head(20))

    # Stage 2
    df_prenatal.columns = df_general.columns
    df_sport.columns = df_general.columns

    df = pd.concat(
        [df_general, df_prenatal, df_sport], ignore_index=True)

    df.drop(columns=['Unnamed: 0'], inplace=True)
    print(df.sample(20))

