import os
import requests
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_absolute_error

from xgboost import XGBRegressor
from lightgbm import early_stopping, LGBMRegressor
from catboost import CatBoostRegressor

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

n_jobs = -1
learning_rate = 1e-1
max_depth = 10
n_estimators = 100
eval_set = [(X_val_norm, y_val)]
stopping_rounds = 5
callbacks = [
    early_stopping(stopping_rounds=stopping_rounds, verbose=False)
]

xgb = XGBRegressor(
    objective='reg:squarederror', n_estiamtors=n_estimators,
    learning_rate=learning_rate, max_depth=max_depth,
    early_stopping=stopping_rounds, verbosity=0, n_jobs=n_jobs
)

lgbm = LGBMRegressor(
    objective='regression', n_estimators=n_estimators,
    learning_rate=learning_rate, max_depth=max_depth,
    verbosity=-1, n_jobs=n_jobs
)

catboost = CatBoostRegressor(
    loss_function='RMSE', iterations=n_estimators,
    learning_rate=learning_rate, max_depth=max_depth,
    early_stopping_rounds=stopping_rounds, silent=True, thread_count=n_jobs
)

# for XGBoost and CatBoost
xgb.fit(X_train_norm, y_train, eval_set=eval_set, verbose=False)
catboost.fit(X_train_norm, y_train, eval_set=eval_set, verbose=False)

# for LightGBM
lgbm.fit(X_train_norm, y_train, eval_set=eval_set, callbacks=callbacks)

result = {
    'xgb_reg': [
        mean_absolute_error(y_train, xgb.predict(X_train_norm)),
        mean_absolute_error(y_val, xgb.predict(X_val_norm)),
        mean_absolute_error(y_test, xgb.predict(X_test_norm))
    ],
    'cat_reg': [
        mean_absolute_error(y_train, catboost.predict(X_train_norm)),
        mean_absolute_error(y_val, catboost.predict(X_val_norm)),
        mean_absolute_error(y_test, catboost.predict(X_test_norm))
    ],
    'lgbm_reg': [
        mean_absolute_error(y_train, lgbm.predict(X_train_norm)),
        mean_absolute_error(y_val, lgbm.predict(X_val_norm)),
        mean_absolute_error(y_test, lgbm.predict(X_test_norm))
    ]
}

mae_df = pd.DataFrame(result, index=['mae_train', 'mae_val', 'mae_test'])
mae_df.to_csv('../data/baseline.csv')
