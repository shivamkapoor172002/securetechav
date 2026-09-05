"""
SecureTech AV Designs — Flask Web Application
Run:  python app.py
"""

from flask import Flask, render_template, send_from_directory, url_for
from flask_compress import Compress
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
Compress(app)

# Cache static assets for 1 year
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 31536000


@app.after_request
def dont_cache_pages(resp):
    """HTML must always be revalidated: a cached page keeps pointing at the old
    image filenames long after the templates change. Static assets keep the
    long max-age set above."""
    if resp.mimetype == "text/html":
        resp.headers["Cache-Control"] = "no-store, must-revalidate"
        resp.headers["Pragma"] = "no-cache"
    return resp

@app.context_processor
def _versioned_static():
    """Append the file's mtime to every static URL.

    Static assets are served with a one-year max-age, so replacing a file in
    place (same name, new bytes) leaves browsers on the old copy indefinitely.
    Stamping ?v=<mtime> makes the URL change whenever the file does, which
    busts the cache for that asset only and keeps the long max-age for the
    rest."""

    def versioned_url_for(endpoint, **values):
        if endpoint == "static":
            filename = values.get("filename")
            if filename:
                try:
                    values["v"] = int(
                        os.stat(os.path.join(app.static_folder, filename)).st_mtime
                    )
                except OSError:
                    pass
        return url_for(endpoint, **values)

    return {"url_for": versioned_url_for}


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


@app.route("/CaseStudies")
def case_studies():
    return render_template("case_studies.html")


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
