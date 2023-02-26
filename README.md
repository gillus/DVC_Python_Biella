# DVC_Python_Biella
Questo repository vuole essere un tutorial sul primo setup e utilizzo del tool Data Version Control.

## Inizializzazione DVC e configurazione remote
Una volta installati i requirements inizializzare DVC utilizzando il comando
```sh
dvc init
```
Per aggiungere un remote (ad esempio cloud su S3) utilizzare il seguente comando
```sh
dvc remote add -d myremote s3://<bucket>/<key>
```
Dove s3:// rappresenta l'indirizzo del bucket da usare come remote (si da per scontato che le autorizzazioni siano state fornite separatamente).

L'inizializzazione crea una cartella da aggiungere al repository (contenente eventuali configurazioni remote effettuate nel passaggio precedente)
```sh
git add .dvc/config .dvc/.gitignore
git commit -m "prima inizializzazione DVC"
git push
```
Per aggiungere un remote (ad esempio cloud su S3) utilizzare il seguente comando
```sh
dvc remote add -d myremote s3://<bucket>/<key>
```
Dove s3:// rappresenta l'indirizzo del bucket da usare come remote (si da per scontato che le autorizzazioni siano state fornite separatamente).

## Aggiunta primo dataset

Per aggiungere un dataset al repository DVC occorre prima rimuovere il dato stesso dal repo git utilizzando il comando:
```sh
git rm data/raw_data.csv 
git commit -m "rimozione dato da git"
git push
```
Seguito da:
```sh
dvc add data/raw_data.csv
```
Il comando crea un file raw_data.csv.dvc da aggiungere al repo git in sostituzione al file originale
```sh
git add data/raw_data.csv.dvc
git commit -m "aggiunto primo dato su DVC"
git push
```
## Creazione di una pipeline machine learning con DVC
Per creare una pipeline DVC creare il file dvc.yaml all'interno della directory principale del repo e copiare il seguente contenuto
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
La pipeline potra' essere riprodotta utilizzando il comando 
```sh
dvc repro
```
Le metriche e i plot possono essere collezionati utilizzando i seguenti comandi
```sh
dvc metrics show
dvc plots show
```

## Creazione di una GitHub Action
Per creare una GitHub action che faccia girare la pipeline ad ogni push sul repository, creare il seguente file (DVC.yaml) all'interno della cartella .github/workflows

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
N.B. Nel file sono specificati i secrets contenenti le credenziali di accesso S3 da aggiungere a livello di repository.


