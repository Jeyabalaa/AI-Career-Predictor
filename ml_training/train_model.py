"""Standalone script to train the career prediction model.

Run this from the project root:
    python ml_training/train_model.py
"""

from predictor.ml_model.train import train_and_save

if __name__ == "__main__":
    model_path = train_and_save()
    print(f"Model trained and saved to {model_path}")
