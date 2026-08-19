import logging
import os
from flask import Flask, render_template, request
from analyzer import PasswordStrengthAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
analyzer = PasswordStrengthAnalyzer()

# ✅ Log the data directory at startup
DATA_DIR = "/app/data"
logger.info(f"Password storage directory: {DATA_DIR}")
print(f"Password storage directory: {DATA_DIR}")  # also prints to stdout

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    suggestion = None
    save_status = None

    if request.method == "POST":
        password = request.form.get("password")
        if "check" in request.form:
            result = analyzer.analyze(password)
            save_status = analyzer.save_password(password)
            logger.info(f"Password analyzed and saved to {DATA_DIR}")
        elif "suggest" in request.form:
            suggestion = analyzer.suggest_password()
            logger.info("Password suggestion generated")

    return render_template("index.html", result=result, suggestion=suggestion, save_status=save_status)

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)