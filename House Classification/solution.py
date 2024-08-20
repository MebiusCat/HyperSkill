import os
import requests
import sys
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier


def review_dataset(house_df):
    # How many rows does the DataFrame have?
    print(house_df.shape[0])
    # How many columns does the DataFrame have?
    print(house_df.columns.shape[0])
    # Are there any missing values in the DataFrame (True or False)?
    print(house_df.isna().sum().sum() > 0)
    # What is the maximum number of rooms across the houses in the dataset?
    print(house_df.Room.max())
    # What is the mean area of the houses in the dataset?
    print(house_df.Area.mean())
    # How many unique values does column Zip_loc contain?
    print(house_df.Zip_loc.nunique())

if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'house_class.csv' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/7vjkrlggmvr5bc1/house_class.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/house_class.csv', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")

    # Stage 1
    df = pd.read_csv('../Data/house_class.csv')
    # review_dataset(df)

    # Stage 2
    X, y = df.loc[:, 'Area':], df.loc[:, 'Price']
    X_train, X_test, y_train, y_test = (
        train_test_split(X, y,
                         random_state=1, test_size=0.3, stratify=df['Zip_loc'].values))
    # print(X_train.Zip_loc.value_counts().to_dict())

    # Stage 3
    enc = OneHotEncoder(drop='first')
    enc.fit(X[['Zip_area', 'Zip_loc', 'Room']])
    X_train_transformed = pd.DataFrame(
        enc.transform(X_train[['Zip_area', 'Zip_loc', 'Room']]).toarray(),
        index=X_train.index)
    X_train_final = X_train[['Area', 'Lon', 'Lat']].join(X_train_transformed)
    X_train_final.rename(columns=str, inplace=True)

    X_test_transformed = pd.DataFrame(
        enc.transform(X_test[['Zip_area', 'Zip_loc', 'Room']]).toarray(),
        index=X_test.index)
    X_test_final = X_test[['Area', 'Lon', 'Lat']].join(X_test_transformed)
    X_test_final.rename(columns=str, inplace=True)

    model = DecisionTreeClassifier(
        criterion='entropy',
        max_features=3,
        splitter='best',
        max_depth=6,
        min_samples_split=4,
        random_state=3)

    model.fit(X_train_final, y_train)

    y_pred = model.predict(X_test_final)
    print(accuracy_score(y_test, y_pred))
