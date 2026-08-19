from flask import Flask, render_template, request
from analyzer import PasswordStrengthAnalyzer

app = Flask(__name__)
analyzer = PasswordStrengthAnalyzer()

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
        elif "suggest" in request.form:
            suggestion = analyzer.suggest_password()

    return render_template("index.html", result=result, suggestion=suggestion, save_status=save_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)