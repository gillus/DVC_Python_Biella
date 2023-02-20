from sklearn.metrics import classification_report
from mlflow.models.signature import infer_signature
import mlflow
from data.datamanager import data_loader


def model_metrics(clf, data_path):

    x_test, y_test = data_loader(data_path)
    metrics = classification_report(y_test, clf.predict(x_test), output_dict=True)

    return metrics


def convert_sklearn_mlflow(clf, x_sample):

    signature = infer_signature(x_sample, clf.predict(x_sample))
    input_example = {}
    for i in x_sample.columns:
        input_example[i] = x_sample[i][0]

    mlflow.sklearn.save_model(clf, "best_model", signature=signature, input_example=input_example)

    return

