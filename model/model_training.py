from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from lightgbm import LGBMClassifier
import json
import os
import joblib
import pandas as pd
import yaml


def data_loader(path: str):
    data_csv_path = path
    dataset = pd.read_csv(data_csv_path)

    target_column = 'income'
    y = dataset[target_column]
    x = dataset.drop(target_column, axis=1)
    return x, y


def train_random_forest_model():
    # This function trains a random folder classifier using the data specified by datapath
    # If parameters are not specified as argument look for params.json file, otherwise create default values
    # if parameters is None:
    #     if os.path.exists('./params.json'):
    #         parameters = json.load(open("params.json", "r"))
    #     else:
    #         parameters = dict(n_estimators=100, max_depth=4, criterion='gini',
    #                           min_sample_leaf=10)
    parameters = yaml.safe_load(open("params.yaml"))["train"]


    print(parameters)
    x_training, y_training = data_loader('./train.csv')
    x_val, y_val = data_loader('./val.csv')

    # Scikit learn ColumnTransformer used to process ordinal and nominal data
    ordinal_features = x_training.select_dtypes(include="number").columns
    categorical_features = x_training.select_dtypes(include="object").columns

    numerical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')),
                                          ('scaler', StandardScaler())])

    categorical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='most_frequent')),
                                              ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    x_encoder = ColumnTransformer(transformers=[('num', numerical_transformer, ordinal_features),
                                                ('cat', categorical_transformer, categorical_features)])

    print(parameters)
    rf_clf = LGBMClassifier(n_estimators=parameters['n_estimators'],
                            max_depth=parameters['max_depth'],
                            random_state=42)

    rf_pipeline = Pipeline(steps=[("preprocessing", x_encoder), ("rf_model", rf_clf)])
    rf_pipeline.fit(x_training, y_training)

    pred_val = rf_pipeline.predict(x_val)
    metrics = classification_report(y_val,pred_val, output_dict=True)
    # serialize model using joblib
    joblib.dump(rf_pipeline, 'model.pkl')
    json.dump(metrics, open("metrics.json", "w"))
    return rf_pipeline


if __name__ == '__main__':

    train_random_forest_model()
