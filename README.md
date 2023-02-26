# DVC_Python_Biella
Questo repository vuole essere un tutorial sul primo setup e utilizzo del tool Data Version Control.

```yaml
stages:
  prepare:
    cmd: python3 data/data_preparation.py
    deps:
    - data/data_preparation.py
    - data/raw_data.csv
    params:
    - prepare.test_size
    - prepare.undersampling
    - prepare.val_size
    outs:
    - holdout.csv
    - train.csv
    - val.csv
  train:
    cmd: python3 model/model_training.py
    deps:
    - model/model_training.py
    - train.csv
    - val.csv
    params:
    - train.criterion
    - train.max_depth
    - train.min_sample_leaf
    - train.n_estimators
    outs:
    - metrics.json
    - model.pkl
  test:
    cmd: python3 -m pytest
    deps:
    - model.pkl    
    - holdout.csv
    - test/test_data_and_model.py
    metrics:
    - rocauc.json:
        cache: true
    outs:
    - prc.json

plots:
  - Precision-Recall:
      template: simple
      x: recall
      y:
        prc.json: precision
```
```yaml
name: DVC  

on: [push]

jobs:
  dvc_repro:
    runs-on: ubuntu-latest
    steps:
        - name: Checkout
          uses: actions/checkout@v2

        - name: Configure AWS credentials
          uses: aws-actions/configure-aws-credentials@v1
          with:
            aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
            aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
            aws-region: eu-central-1

        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
            pip install -e .
        - name: DVC
          run: |
            dvc pull
            dvc repro
```            
