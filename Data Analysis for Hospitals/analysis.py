import pandas as pd

if __name__ == '__main__':
    pd.set_option('display.max_columns', 8)

    df_general = pd.read_csv('test/general.csv')
    df_prenatal = pd.read_csv('test/prenatal.csv')
    df_sport = pd.read_csv('test/sports.csv')

    print(df_general.head(20))
    print(df_prenatal.head(20))
    print(df_sport.head(20))
