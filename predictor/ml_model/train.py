import os
import pickle

import pandas as pd
from sklearn.tree import DecisionTreeClassifier


def get_model_path():
    return os.path.join(os.path.dirname(__file__), "career_model.pkl")


def get_dataset_path():
    # Dataset is expected in the project root under ml_training/dataset.csv
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(root, "ml_training", "dataset.csv")


def train_and_save(model_path=None, dataset_path=None):
    """Train a simple model and save it to disk."""
    model_path = model_path or get_model_path()
    dataset_path = dataset_path or get_dataset_path()

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    data = pd.read_csv(dataset_path)
    X = data[["coding", "math", "creativity", "communication"]]
    y = data["career"]

    model = DecisionTreeClassifier()
    model.fit(X, y)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    return model_path
