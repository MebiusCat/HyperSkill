import numpy as np
import pandas as pd
import os
import requests


def clean_data(data_path):
    df = pd.read_csv(data_path)
    df['b_day'] = pd.to_datetime(df['b_day'], format='%m/%d/%y')
    df['draft_year'] = pd.to_datetime(df['draft_year'], format='%Y')
    df['team'] = df['team'].fillna('No Team')
    df['height'] = df['height'].apply(lambda x: x.split('/')[1]).astype(float)
    df['weight'] = (df['weight']
                    .apply(lambda x: x.split('/')[1].replace('kg.', ''))
                    .astype(float))
    df['salary'] = df['salary'].str.strip('$').astype(float)
    df['country'] = df['country'].apply(lambda x: 'USA' if x == 'USA' else 'Not-USA')
    df['draft_round'] = df['draft_round'].replace('Undrafted', '0')

    return df

def feature_data(df):
    df['version'] = np.where(df['version'] == 'NBA2k20', 2020, 2021)
    df['age'] = (pd.to_datetime(df['version'], format='%Y') - df['b_day']).dt.days / 365.25
    df['age'] = df['age'].astype(int) + 1
    df['experience'] =\
        (pd.to_datetime(df['version'], format='%Y') - df['draft_year']).dt.days / 365
    df['experience'] = df['experience'].astype(int)
    df['bmi'] = df['weight'] / df['height'] ** 2

    df.drop(columns=['version', 'b_day', 'draft_year', 'weight', 'height'], inplace=True)
    df.drop(columns=['full_name', 'jersey', 'draft_peak', 'college'], inplace=True)
    return df

# Checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# Download data if it is unavailable.
if 'nba2k-full.csv' not in os.listdir('../Data'):
    print('Train dataset loading.')
    url = "https://www.dropbox.com/s/wmgqf23ugn9sr3b/nba2k-full.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/nba2k-full.csv', 'wb').write(r.content)
    print('Loaded.')

data_path = "../Data/nba2k-full.csv"

df_cleaned = clean_data(data_path)
df = feature_data(df_cleaned)

print(df[['age', 'experience', 'bmi']].head())