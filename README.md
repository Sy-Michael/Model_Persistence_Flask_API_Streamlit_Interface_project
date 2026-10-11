Student Pass Prediction — Model Persistence and Deployment
This project demonstrates the three activities from the lesson:

Model persistence: train a simple model and save/load it with joblib.
Flask API: accept JSON input, validate values, and return a JSON prediction.
Streamlit interface: provide a small interactive page to enter a student name and study hours.
Educational demo only. The sample dataset is illustrative and should not be used to make real decisions about students.

1. Requirements
Python 3.10 or newer
Internet access the first time you install the Python packages
Open a terminal in this folder and create a virtual environment (recommended):

Windows
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
If PowerShell blocks activation, you can use Command Prompt:

.venv\Scripts\activate.bat
2. Train and save the model
python train_model.py
This creates student_pass_model.joblib in this folder and prints three example predictions. The Flask and Streamlit apps load this file; they do not retrain the model when a prediction is requested.

3. Run the Flask API
In Terminal 1:

python app.py
The API runs at http://127.0.0.1:5000.

Open http://127.0.0.1:5000/ in a browser to see the API information.

Test with curl.exe (Windows)
In Terminal 2:

curl.exe -X POST http://127.0.0.1:5000/predict `
  -H "Content-Type: application/json" `
  -d "{\"study_hours\":4.5,\"attendance_percentage\":92}"
Example response:

{
  "study_hours": 4.5,
  "attendance_percentage": 92.0,
  "prediction": "Pass",
  "note": "Prediction is based on study_hours only. Attendance is validated and reported but is not a model feature."
}
Try invalid values too:

curl.exe -X POST http://127.0.0.1:5000/predict `
  -H "Content-Type: application/json" `
  -d "{\"study_hours\":30,\"attendance_percentage\":92}"
This should return HTTP 400 with an error message.

4. Run the Streamlit app
Stop the Flask server with Ctrl+C, or open another terminal. Run:

streamlit run streamlit_app.py
Streamlit will show a local URL, usually http://localhost:8501. Enter a student name, set study hours, and click Predict result.

5. Project files
StudentPassPrediction/
├── train_model.py             # trains, saves, loads, and tests the model
├── student_pass_model.joblib  # generated after training
├── app.py                     # Flask JSON API
├── streamlit_app.py           # Streamlit interface and sample chart
├── requirements.txt           # Python dependencies
└── README.md                  # setup and run instructions
Important note about attendance
The lesson's example model uses study hours only. This exercise's API accepts and validates attendance_percentage and returns it in the JSON response, but it does not affect the prediction. If attendance must influence the result, add attendance as a second input feature in train_model.py, train on a suitable dataset containing both features, save the new model, and update the API prediction input to pass both values.