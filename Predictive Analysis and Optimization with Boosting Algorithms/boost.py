import os
import requests
import pandas as pd

def download_data():
    # Create data directory
    if not os.path.exists('../data'):
        os.mkdir('../data')

    # Download data if it is unavailable
    if 'insurance.csv' not in os.listdir('../data'):
        url = "https://www.dropbox.com/scl/fi/r5033u0e89bpjrk3n9snx/insurance.csv?rlkey=8sv6cnesc6kkqmu6jrizvn9ux&dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../data/insurance.csv', 'wb').write(r.content)


download_data()
df = pd.read_csv('../data/insurance.csv')
df.drop_duplicates(inplace=True)

num_feature = df.select_dtypes('number').columns.tolist()
cat_feature = df.select_dtypes('object').columns.tolist()

answer = {
    'numerical': num_feature,
    'categorical': cat_feature,
    'shape': list(df.shape)
}
print(answer)
