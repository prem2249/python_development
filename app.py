from flask import Flask, render_template, request
import pickle
import os
import pandas as pd
from utils import extract_text_from_pdf, extract_text_from_csv, extract_text_from_txt

app = Flask(__name__)

# Load model + vectorizer
model = pickle.load(open("phishing_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        email_text = ""

        # Case 1: Direct text input
        if "email" in request.form and request.form["email"].strip():
            email_text = request.form["email"]

        # Case 2: File upload
        elif "file" in request.files and request.files["file"].filename != "":
            file = request.files["file"]
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            if file.filename.endswith(".pdf"):
                email_text = extract_text_from_pdf(file_path)
            elif file.filename.endswith(".csv"):
                email_text = extract_text_from_csv(file_path)
            elif file.filename.endswith(".txt"):
                email_text = extract_text_from_txt(file_path)

        # Case 3: Fallback → use sample dataset.csv
        else:
            df = pd.read_csv("data/dataset.csv")
            email_text = " ".join(df['text'].astype(str).values)

        # Run prediction
        if email_text.strip():
            features = vectorizer.transform([email_text])
            prediction = model.predict(features)[0]
            result = "Phishing 🚨" if prediction == "phishing" else "Safe ✅"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)