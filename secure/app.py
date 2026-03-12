"""
SecureTech AV Designs — Flask Web Application
Run:  python app.py
"""

from flask import Flask, render_template, send_from_directory
from flask_compress import Compress
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
Compress(app)

# Cache static assets for 1 year
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 31536000

WELL_KNOWN_DIR = os.path.join(app.static_folder, ".well-known")


# ── PAGES ──

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


# ── SEO & CRAWLABILITY ──

@app.route("/robots.txt")
def robots():
    return send_from_directory(app.static_folder, "robots.txt", mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(app.static_folder, "sitemap.xml", mimetype="application/xml")


@app.route("/feed.xml")
def feed():
    return send_from_directory(app.static_folder, "feed.xml", mimetype="application/rss+xml")


# ── AI / LLM DISCOVERABILITY ──

@app.route("/llms.txt")
def llms():
    return send_from_directory(app.static_folder, "llms.txt", mimetype="text/plain")


@app.route("/.well-known/llms.txt")
def llms_well_known():
    return send_from_directory(app.static_folder, "llms.txt", mimetype="text/plain")


@app.route("/.well-known/ai-plugin.json")
def ai_plugin():
    return send_from_directory(WELL_KNOWN_DIR, "ai-plugin.json", mimetype="application/json")


@app.route("/.well-known/wacp.json")
def wacp():
    return send_from_directory(WELL_KNOWN_DIR, "wacp.json", mimetype="application/json")


@app.route("/.well-known/security.txt")
def security():
    return send_from_directory(WELL_KNOWN_DIR, "security.txt", mimetype="text/plain")


@app.route("/.well-known/ai.txt")
def ai_txt():
    return send_from_directory(WELL_KNOWN_DIR, "ai.txt", mimetype="text/plain")


@app.route("/.well-known/skills.json")
def skills():
    return send_from_directory(WELL_KNOWN_DIR, "skills.json", mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
