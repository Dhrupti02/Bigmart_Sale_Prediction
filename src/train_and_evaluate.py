from get_data import read_params
import argparse
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
import json
import os
import joblib
import logging

''' Train the data and evaluate the performance of the model. '''

# Performance matrices
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def train_and_evaluate(config_path):
    logger = logging.getLogger("train_and_evaluate")
    config = read_params(config_path)
    test_data_path = config["split_data"]["test_path"]
    train_data_path = config["split_data"]["train_path"]
    random_state = config["base"]["random_state"]
    model_dir = config["model_dir"]

    n_estimators = config["estimators"]["RandomForestRegressor"]["params"]["n_estimators"]
    max_features = config["estimators"]["RandomForestRegressor"]["params"]["max_features"]
    max_depth = config["estimators"]["RandomForestRegressor"]["params"]["max_depth"]
    min_samples_split = config["estimators"]["RandomForestRegressor"]["params"]["min_samples_split"]
    min_samples_leaf = config["estimators"]["RandomForestRegressor"]["params"]["min_samples_leaf"]

    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
                'max_features': max_features,
                'max_depth': max_depth,
                'min_samples_split': min_samples_split,
                'min_samples_leaf': min_samples_leaf}

    target = [config["base"]["target_col"]]

    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")

    train_y = train[target]
    test_y = test[target]

    train_x = train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)


    # Use the random grid to search for best hyperparameters
    # First create the base model to tune
    rf = RandomForestRegressor()
    # Random search of parameters, using 3 fold cross validation, 
    # search across 100 different combinations
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid,scoring='neg_mean_squared_error', random_state = random_state, n_iter = 10, cv = 5, verbose=2, n_jobs = 1)
    rf_random.fit(train_x, train_y)
    predictions = rf_random.predict(test_x)
    (rmse, mae, r2) = eval_metrics(test_y, predictions)
    logger.info('> RMSE: %.2f' % rmse)
    logger.info('> MAE: %.2f' % mae)
    logger.info('> R2: %.2f' % r2)


    scores_file = config["reports"]["scores"]
    params_file = config["reports"]["params"]

    with open(scores_file, "w") as f:
        scores = {
            "rmse": rmse,
            "mae": mae,
            "r2": r2
        }
        json.dump(scores, f, indent=4)

    with open(params_file, "w") as f:
        params = {
               'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
        }
        json.dump(params, f, indent=4)

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")

    joblib.dump(rf_random, model_path)
    
# Create logger and assign handler
logger = logging.getLogger("train_and_evaluate")
handler  = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s|%(levelname)s|%(name)s|%(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger = logging.getLogger("train_and_evaluate.iter")
logger.setLevel(logging.INFO)


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)