"""
Train a simple student pass/fail model and save it with joblib.
The model uses study_hours only, matching the lesson example.
"""
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "student_pass_model.joblib"


def main():
    # Illustrative sample data for learning purposes:
    # study hours per day -> 0 = Fail, 1 = Pass
    study_hours = np.array([
        [0.5], [1.0], [1.5], [2.0], [2.5],
        [3.0], [3.5], [4.0], [4.5], [5.0],
        [5.5], [6.0], [6.5], [7.0], [8.0]
    ])
    passed = np.array([0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1])

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(random_state=42))
    ])
    model.fit(study_hours, passed)

    joblib.dump(model, MODEL_PATH)
    print(f"Model trained and saved to: {MODEL_PATH}")

    # Demonstrate loading the saved model and predicting without retraining.
    loaded_model = joblib.load(MODEL_PATH)
    test_hours = np.array([[2.0], [4.0], [6.0]])
    predictions = loaded_model.predict(test_hours)

    print("\nExample predictions:")
    for hours, prediction in zip(test_hours.ravel(), predictions):
        label = "Pass" if int(prediction) == 1 else "Fail"
        print(f"Study hours: {hours:.1f} -> Predicted result: {label}")


if __name__ == "__main__":
    main()