from flask import Flask, request, render_template, send_file
from port_scanner import normalize_target, resolve_target, full_port_scan, generate_report_text, save_report

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["target"]
        mode = request.form.get("mode", "common")
        start = int(request.form.get("start", 1))
        end = int(request.form.get("end", 1024))
        custom_ports_str = request.form.get("custom_ports", "")
        custom_ports = [int(p.strip()) for p in custom_ports_str.split(",") if p.strip().isdigit()]

        target = normalize_target(user_input)
        ip = resolve_target(target)

        if ip:
            open_ports = full_port_scan(ip, mode=mode, start=start, end=end, custom_ports=custom_ports)
        else:
            open_ports = {}

        report_text = generate_report_text(target, open_ports)
        filename = save_report(target, report_text)

        return render_template("index.html", report=report_text, filename=filename)

    return render_template("index.html", report=None)

@app.route("/download/<path:filename>")
def download(filename):
    return send_file(filename, as_attachment=True)

# Below is the code to run the Flask app. This should be placed at the end of your webapp.py file. 
# it will start the Flask development server when you run the script directly. 
# If you want run service on a public IP, you can change the host to ' app.run(host="0.0.0.0", port=5000, debug=True)
# If you want run service on localhost only, you can change the host to ' app.run(host="127.0.0.1", port=5000, debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)