import os
import requests
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

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

X, y = df.drop(columns=['charges']), df['charges']

num_features = X.select_dtypes('number').columns.tolist()
cat_features = X.select_dtypes('object').columns.tolist()

threshod = 3
z = abs(y - y.mean()) / y.std()
X, y = X[z < threshod], y[z < threshod]

X_part, X_test, y_part, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=10)
X_train, X_val, y_train, y_val = train_test_split(X_part, y_part, test_size=0.2, shuffle=True, random_state=10)

ct = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(), cat_features)
    ]
)

ct.fit(X_train)
X_train_norm = ct.transform(X_train)
X_test_norm = ct.transform(X_test)
X_val_norm = ct.transform(X_val)

answer = {
    'train': list(X_train_norm.shape),
    'validation': list(X_val_norm.shape),
    'test': list(X_test_norm.shape)
}
print(answer)