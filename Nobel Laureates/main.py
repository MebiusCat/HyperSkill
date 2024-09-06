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

    print(df.born_in.tolist())
