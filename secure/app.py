"""
SecureTech AV Designs — Flask Web Application
Run:  python app.py
"""

from flask import (Flask, abort, redirect, render_template, request, session,
                   send_from_directory, url_for)
from flask_compress import Compress
import hmac
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

# The Workspace Designer is a self-contained static bundle (~100 MB of 3D
# models and textures) that lives OUTSIDE this package on purpose: on Vercel
# it is served straight from the CDN by a @vercel/static build, so it never
# enters the Python function's size budget. This route exists so `python
# app.py` serves it too during local development.
WORKSPACE_DIR = os.path.join(os.path.dirname(app.root_path), "workspace")


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


# ── WORKSPACE DESIGNER ──

# ── DESIGNER ACCESS ──
#
# The room list is public; the designer behind it is not. The gate has to be
# here rather than in the browser, because the designer is a static bundle -
# anything checked in page script is bypassable by reading that script.
#
# The fallback below is set at the owner's instruction. This repository is
# public, so that value is readable by anyone who looks: it keeps the designer
# out of casual reach, it is not a secret. Setting SECURETECH_ADMIN_PASSWORD in
# the environment overrides it without a code change, which is where a real
# secret belongs.
ADMIN_PASSWORD = os.environ.get("SECURETECH_ADMIN_PASSWORD") or "nahibataraha"
app.secret_key = os.environ.get("SECURETECH_SECRET_KEY") or os.urandom(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

# slug -> (SecureTech name, capacity, card image, category)
ROOMS = [
    ("huddleroom",     "Focus Pod",          "2-4",    "Huddle-Room.webp",     "Conference Rooms"),
    ("smallroom",      "Mini Board Room",    "4-6",    "Small-Room.webp",      "Conference Rooms"),
    ("mediumroom",     "Medium Board Room",  "6-10",   "Medium-Room.webp",     "Conference Rooms"),
    ("largeroom",      "Large Board Room",   "11-24",  "Large-Room.webp",      "Conference Rooms"),
    ("boardroom",      "Leadership Hub",     "11-24",  "Boardroom.webp",       "Conference Rooms"),
    ("ideationspace",  "Innovation Hub",     "3-10",   "ideation-space.webp",  "Conference Rooms"),
    ("personaldesk",   "Workstation",        "1",      "personal-desk.webp",   "Office Rooms"),
    ("openspace",      "Collab Area",        "1",      "openspace.webp",       "Office Rooms"),
    ("focusroom",      "Huddle Room",        "1-2",    "focus-room.webp",      "Office Rooms"),
    ("trainingroom",   "Multi Purpose Hall", "10-50",  "trainingroom.webp",    "Large Venue"),
    ("auditorium",     "Auditorium",         "20-150", "auditorium.webp",      "Large Venue"),
]
CATEGORIES = ["Conference Rooms", "Office Rooms", "Large Venue"]
ROOM_SLUGS = {slug for slug, *_ in ROOMS}


def _signed_in():
    return session.get("designer") is True


@app.route("/WorkspaceDesigner")
def workspace_designer():
    """The public room list. Browsing is open to anyone; opening a room is not."""
    return render_template("designer_rooms.html", rooms=ROOMS, categories=CATEGORIES,
                           signed_in=_signed_in())


@app.route("/WorkspaceDesigner/enter/<room>", methods=["GET", "POST"])
def workspace_enter(room):
    """Password gate in front of one room, then the designer itself."""
    if room not in ROOM_SLUGS:
        abort(404)
    error = None
    if request.method == "POST":
        supplied = request.form.get("password", "")
        if not ADMIN_PASSWORD:
            error = "The designer is not configured for access yet."
        elif hmac.compare_digest(supplied, ADMIN_PASSWORD):
            session["designer"] = True
            return redirect(url_for("workspace_enter", room=room))
        else:
            error = "That password was not recognised."
    if _signed_in():
        return render_template("workspace.html", room=room)
    return render_template("designer_login.html", room=room, error=error,
                           room_name=next(n for s, n, *_ in ROOMS if s == room)), (
        401 if error else 200)


@app.route("/WorkspaceDesigner/signout")
def workspace_signout():
    session.pop("designer", None)
    return redirect(url_for("workspace_designer"))


@app.route("/fontdata/<path:filename>")
def workspace_fontdata(filename):
    """The 3D text renderer resolves its font data from
    `self.location.origin + "/fontdata"` inside a web worker, so this one
    bundle path is origin-rooted no matter where the app is mounted. Serving
    it here is more durable than patching the minified bundle, which a future
    re-snapshot would undo."""
    return send_from_directory(os.path.join(WORKSPACE_DIR, "fontdata"), filename,
                               max_age=31536000)


@app.route("/workspace/")
@app.route("/workspace/<path:filename>")
def workspace_static(filename="index.html"):
    # Withholding the shell is what actually closes the designer: the assets
    # below it are inert without the page that boots them.
    if filename in ("", "index.html") and not _signed_in():
        return redirect(url_for("workspace_designer"))

    # The bundle's own entry files change whenever the local adaptation does,
    # and they carry no content hash, so they must revalidate. The hashed
    # build output and the 3D assets keep the long cache.
    volatile = filename.endswith((".html", "local-adapter.js", "local-adapter.css",
                                  "manifest.json"))
    return send_from_directory(WORKSPACE_DIR, filename,
                               max_age=0 if volatile else 31536000)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
