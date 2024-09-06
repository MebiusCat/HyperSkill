import matplotlib.pyplot as plt
import pandas as pd
import os
import requests
import sys


def get_place(row):
    if row['place_of_birth'] and ',' in row['place_of_birth']:
        row['place_of_birth'] = row['place_of_birth'].split(',')[-1].strip()
    else:
        row['place_of_birth'] = None
    if not row['born_in']:
        row['born_in'] = row['place_of_birth']
    return row


if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/Nobel_laureates.json', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")

    df = pd.read_json('../Data/Nobel_laureates.json')

    # Stage 1
    # print(max(df.duplicated()))
    df = df.dropna(subset='gender')
    df = df.reset_index(drop=True)
    # print(df.head(20)[['country', 'name']].to_dict())

    # Stage 2
    df = df.apply(get_place, axis=1)
    df = df.dropna(subset='born_in')
    df = df.reset_index(drop=True)
    df.born_in = df.born_in.replace(['US', 'United States', 'U.S.'], 'USA')
    df.born_in = df.born_in.replace('United Kingdom', 'UK')
    # print(df.born_in.tolist())

    # Stage 3
    df['year_born'] = df['date_of_birth'].str.extract(r'(\d{4})', expand=False).astype(int)
    df['age_of_winning'] = df['year'] - df['year_born']
    # print(df.year_born.to_list(), df.age_of_winning.to_list(), sep='\n')

    # Stage 4
    countries_more_25 = df.groupby(['born_in']).agg({'year': 'count'}).query('year >= 25').index

    df['country_display'] = df['born_in'].apply(
        lambda x: x if x in countries_more_25 else 'Other countries')

    data = df.country_display.value_counts()
    colors = ['blue', 'orange', 'red', 'yellow', 'green', 'pink', 'brown', 'cyan', 'purple']
    exp_countries = ['Poland', 'Canada', 'Austria', 'Russia', 'France', 'UK']
    explode = [0.08 if x in exp_countries else 0 for x in data.index]

    fig, axes = plt.subplots(figsize=(12, 12))

    plt.pie(data,
            labels=data.index,
            colors=colors,
            explode=explode,
            autopct=lambda p: "{:.2f}%\n({:.0f})".format(p * sum(data) / 100, p))
    plt.show()
