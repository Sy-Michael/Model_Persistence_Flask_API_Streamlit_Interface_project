"""
Flask API for the saved student pass/fail model.

POST /predict JSON:
{
    "study_hours": 4.5,
    "attendance_percentage": 92
}

Important: the lesson's model uses study_hours only. Attendance is validated
and returned in the response, but does not affect the prediction unless you
add attendance to the training features and retrain the model.
"""
from pathlib import Path

import joblib
from flask import Flask, jsonify, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "student_pass_model.joblib"

app = Flask(__name__)

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}. Run 'python train_model.py' first."
    )

model = joblib.load(MODEL_PATH)


@app.get("/")
def home():
    return jsonify({
        "message": "Student Pass Prediction API",
        "endpoint": "POST /predict",
        "required": {"study_hours": "number from 0 to 24"},
        "optional": {"attendance_percentage": "number from 0 to 100"}
    })


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    if "study_hours" not in data:
        return jsonify({"error": "Missing required field: study_hours."}), 400

    try:
        study_hours = float(data["study_hours"])
    except (TypeError, ValueError):
        return jsonify({"error": "study_hours must be a number."}), 400

    if not 0 <= study_hours <= 24:
        return jsonify({"error": "study_hours must be between 0 and 24."}), 400

    attendance = data.get("attendance_percentage")
    if attendance is not None:
        try:
            attendance = float(attendance)
        except (TypeError, ValueError):
            return jsonify({"error": "attendance_percentage must be a number."}), 400
        if not 0 <= attendance <= 100:
            return jsonify({
                "error": "attendance_percentage must be between 0 and 100."
            }), 400

    prediction = int(model.predict([[study_hours]])[0])
    result = "Pass" if prediction == 1 else "Fail"

    response = {
        "study_hours": study_hours,
        "attendance_percentage": attendance,
        "prediction": result,
        "note": (
            "Prediction is based on study_hours only. "
            "Attendance is validated and reported but is not a model feature."
        )
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)