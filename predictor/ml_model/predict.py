
import os
import pickle

from .train import train_and_save


def _get_model_path():
    return os.path.join(os.path.dirname(__file__), "career_model.pkl")


def predict_career(data):
    model_path = _get_model_path()

    if not os.path.exists(model_path):
        # Train the model automatically if it does not exist.
        try:
            train_and_save(model_path=model_path)
        except Exception as exc:
            return f"Model not trained yet: {exc}"

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    prediction = model.predict([data])
    return prediction[0]
