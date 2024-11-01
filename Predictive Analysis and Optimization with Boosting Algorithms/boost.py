import os
import requests
import numpy as np
import pandas as pd
import optuna

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


def pure_fit():
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


random_state = 10


def xgb_objective(trial):

    # set the hyperparameters
    xgb_hyperparams = {
      'n_estimators': trial.suggest_int('n_estimators', 25, 1000),
      'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-1, log=True),
      'max_depth': trial.suggest_int('max_depth', 2, 20),
      'colsample_bylevel': trial.suggest_float('colsample_bylevel', 0, 1),
      'colsample_bytree': trial.suggest_float('colsample_bytree', 0, 1),
      'objective': trial.suggest_categorical('objective',
                                             ['reg:squarederror', 'reg:gamma', 'reg:absoluteerror', 'reg:tweedie']),
      'alpha': trial.suggest_float('alpha', 0, 5),
      'lambda': trial.suggest_float('lambda', 0, 5),
      'subsample': trial.suggest_float('subsample', 0, 1),
      'tweedie_variance_power': trial.suggest_float('tweedie_variance_power', 1, 2)
    }

    # create an instance of the model with the hyperparameters
    model = XGBRegressor(n_jobs=n_jobs, seed=random_state, verbosity=0,
                         early_stopping_rounds=stopping_rounds, **xgb_hyperparams)

    # fit the model on the train set and evaluate on the validation set
    model.fit(X_train_norm, y_train, eval_set=eval_set, verbose=False)

    # predict with the model
    ypred = model.predict(X_val_norm)

    # estimate the evaluation metric
    mae = mean_absolute_error(y_val, ypred)

    return mae


def catboost_objective(trial):
    # set the hyperparameters
    catboost_hyperparams = {
        'iterations': trial.suggest_int('iterations', 100, 1000),
        'loss_function': trial.suggest_categorical('loss_function',
                                                   ['RMSE', 'MAE', 'MAPE', 'Tweedie:variance_power=1.99']),
        'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-1, log=True),
        'colsample_bylevel': trial.suggest_float('colsample_bylevel', 0, 1),
        'max_depth': trial.suggest_int('max_depth', 2, 16),
        'reg_lambda': trial.suggest_float('reg_lambda', 0, 5),
        'min_child_samples': trial.suggest_int('min_child_samples', 1, 10),
        'subsample': trial.suggest_float('subsample', 0.01, 1),
    }

    # create an instance of the model with the hyperparameters
    model = CatBoostRegressor(thread_count=n_jobs,
                              early_stopping_rounds=stopping_rounds, **catboost_hyperparams)


    # fit the model on the train set and evaluate on the validation set
    model.fit(X_train_norm, y_train, eval_set=eval_set, verbose=False)

    # predict with the model
    ypred = model.predict(X_val_norm)

    # estimate the evaluation metric
    mae = mean_absolute_error(y_val, ypred)

    return mae


def lgbm_objective(trial):

    # set the hyperparameters
    lgbm_hyperparams = {
        'n_estimators': trial.suggest_int('n_estimators', 25, 1000),
        'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-1, log=True),
        'max_depth': trial.suggest_int('max_depth', 2, 20),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0, 1),
        'objective': trial.suggest_categorical('objective', ['regression', 'gamma']),
        'reg_alpha': trial.suggest_float('reg_alpha', 0, 5),
        'reg_lambda': trial.suggest_float('reg_lambda', 0, 5),
        'subsample': trial.suggest_float('subsample', 0, 1),
        'min_child_weight': trial.suggest_float('min_child_weight', 1e-5, 1.0, log=True),
        'min_child_samples': trial.suggest_int('min_child_samples', 2, 30)
    }

    # create an instance of the model with the hyperparameters
    model = LGBMRegressor(n_jobs=n_jobs, seed=random_state, verbosity=-1, **lgbm_hyperparams)

    # fit the model on the train set and evaluate on the validation set
    model.fit(X_train_norm, y_train, eval_set=eval_set, callbacks=callbacks)

    # predict with the model
    ypred = model.predict(X_val_norm)

    # estimate the evaluation metric
    mae = mean_absolute_error(y_val, ypred)

    return mae


# XGB
xgb_study = optuna.create_study(direction='minimize', sampler=optuna.samplers.TPESampler(seed=random_state))
xgb_study.optimize(xgb_objective, n_trials=500, n_jobs=-1)

base_score = np.mean(y_train)
xgb_opt = XGBRegressor(early_stopping_rounds=stopping_rounds, verbosity=0,
                       n_jobs=n_jobs, base_score=base_score, **xgb_study.best_params)
xgb_opt.fit(X_train_norm, y_train, eval_set=eval_set, verbose=False)

# Catboost
catb_study = optuna.create_study(direction='minimize', sampler=optuna.samplers.TPESampler(seed=random_state))
catb_study.optimize(catboost_objective, n_trials=500)

catb_opt = CatBoostRegressor(early_stopping_rounds=stopping_rounds,
                             thread_count=n_jobs, **catb_study.best_params)
catb_opt.fit(X_train_norm, y_train, eval_set=eval_set, verbose=False)

# LightGBM
lgbm_study = optuna.create_study(direction='minimize', sampler=optuna.samplers.TPESampler(seed=random_state))
lgbm_study.optimize(lgbm_objective, n_trials=500, n_jobs=-1)

base_score = np.mean(y_train)
lgbm_opt = LGBMRegressor(verbosity=-1, n_jobs=n_jobs, **lgbm_study.best_params)
lgbm_opt.fit(X_train_norm, y_train, eval_set=eval_set, callbacks=callbacks)

result = {
    'xgb_reg': [
        mean_absolute_error(y_train, xgb_opt.predict(X_train_norm)),
        mean_absolute_error(y_val, xgb_opt.predict(X_val_norm)),
        mean_absolute_error(y_test, xgb_opt.predict(X_test_norm))
    ],
    'cat_reg': [
        mean_absolute_error(y_train, catb_opt.predict(X_train_norm)),
        mean_absolute_error(y_val, catb_opt.predict(X_val_norm)),
        mean_absolute_error(y_test, catb_opt.predict(X_test_norm))
    ],
    'lgbm_reg': [
        mean_absolute_error(y_train, lgbm_opt.predict(X_train_norm)),
        mean_absolute_error(y_val, lgbm_opt.predict(X_val_norm)),
        mean_absolute_error(y_test, lgbm_opt.predict(X_test_norm))
    ]
}

mae_df = pd.DataFrame(result, index=['mae_train', 'mae_val', 'mae_test'])
mae_df.to_csv('../data/optimized.csv')
