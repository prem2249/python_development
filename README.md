# Phishing Email Detection

This project demonstrates a simple machine learning model for detecting phishing emails using **Scikit‑learn**.  
It uses **CountVectorizer** for feature extraction and a **Naive Bayes classifier**, achieving ~83% accuracy on the sample dataset.

---

## 🚀 Features
- Train on a dataset of phishing and legitimate emails (`dataset.csv`).
- Extract textual features (keywords, URLs, suspicious phrases).
- Classify emails as **Phishing 🚨** or **Safe ✅**.
- Display **accuracy** and a **confusion matrix**.
- Flask UI to:
  - Paste email text directly.
  - Upload files (`CSV`, `TXT`, `PDF`).
  - Fallback to sample dataset if no input is provided.

---

## 📂 Project Structure
phishing-email-detector/
│── app.py                # Flask UI
│── model.py              # Training script (Naive Bayes)
│── utils.py              # File parsing + feature extraction
│── requirements.txt       # Dependencies
│── data/
│   └── dataset.csv        # Training dataset
│── templates/
│   └── index.html         # Web UI
│── static/
│   └── style.css          # Styling
│   └── confusion_matrix.png



---

## ⚙️ Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/phishing-email-detector.git
   cd phishing-email-detector

2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Train the model:
python model.py

This generates:

phishing_model.pkl

vectorizer.pkl

static/confusion_matrix.png

5. Run the Flask app:
python app.py
