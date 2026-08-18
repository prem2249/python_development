from flask import Flask, render_template, request
from analyzer import PasswordStrengthAnalyzer

app = Flask(__name__)
analyzer = PasswordStrengthAnalyzer()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    suggestion = None

    if request.method == "POST":
        password = request.form.get("password")
        if "check" in request.form:
            result = analyzer.analyze(password)
        elif "suggest" in request.form:
            suggestion = analyzer.suggest_password()
        analyzer.save_password(password)

    return render_template("index.html", result=result, suggestion=suggestion)

if __name__ == "__main__":
    app.run(debug=True)