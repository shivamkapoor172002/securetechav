"""
SecureTech AV Designs — Flask Web Application
Run:  python app.py
"""

from flask import Flask, render_template, send_from_directory
from flask_compress import Compress

app = Flask(__name__, static_folder='static', static_url_path='/static')
Compress(app)

# Cache static assets for 1 year
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 31536000


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/AboutUs")
def about():
    return render_template("about.html")


@app.route("/Contactus")
def contact():
    return render_template("contact.html")


@app.route("/Solutionpage")
def solutions():
    return render_template("solutions.html")


@app.route("/CorporateProfile")
def corporate_profile():
    return render_template("securetech_profile.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
