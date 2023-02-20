import pandas as pd
import json
import os
import numpy as np
from sklearn.model_selection import train_test_split
import yaml


def prepare_data(data_path: str):
    # This function trains a random folder classifier using the data specified by datapath
    parameters = yaml.safe_load(open("params.yaml"))["prepare"]

    raw_data = pd.read_csv(data_path)

    data = raw_data.iloc[:int(raw_data.shape[0]*(1-parameters['test_size'])), :]
    holdout_data = raw_data.iloc[int(raw_data.shape[0]*(1-parameters['test_size'])):, :]
    train_data, val_data = train_test_split(data, test_size=parameters['val_size'], random_state=42)    

    x1 = train_data[train_data['income']=='>50k']
    x2 = train_data[train_data['income']!='>50k']
    train_data = pd.concat([x1, x2.sample(frac=parameters['undersampling'], random_state=42)], 
                           axis=0).sample(frac=1., random_state=42)

    train_data.to_csv('train.csv', index=False)
    val_data.to_csv('val.csv', index=False)
    holdout_data.to_csv('holdout.csv', index=False)

    return 


if __name__ == '__main__':

    prepare_data('./data/raw_data.csv')
