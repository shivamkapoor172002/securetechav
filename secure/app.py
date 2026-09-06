"""
SecureTech AV Designs — Flask Web Application
Run:  python app.py
"""

from flask import Flask, render_template, request, send_from_directory, url_for
from flask_compress import Compress
import hashlib
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

@app.route("/WorkspaceDesigner")
def workspace_designer():
    """The designer itself is a full-screen SPA, so it is framed inside a page
    that carries the site header rather than replacing it."""
    return render_template("workspace.html")


@app.route("/fontdata/<path:filename>")
def workspace_fontdata(filename):
    """The 3D text renderer resolves its font data from
    `self.location.origin + "/fontdata"` inside a web worker, so this one
    bundle path is origin-rooted no matter where the app is mounted. Serving
    it here is more durable than patching the minified bundle, which a future
    re-snapshot would undo."""
    return send_from_directory(os.path.join(WORKSPACE_DIR, "fontdata"), filename,
                               max_age=31536000)


# The room's 3D surfaces (walls, floor, ceiling, carpet) live in a
# react-three-fiber scene that the bundle never exposes: the room page renders
# ~144 DOM nodes and r3f keeps its scene in its own reconciler, so no amount of
# DOM/fiber walking from local-adapter.js can reach it. The bundle does hold one
# spot where the scene is already in a local variable - the wall-visibility
# component's `useThree()` destructure - so the scene is published from there.
#
# The injection happens while serving, so the vendored bundle on disk stays
# byte-for-byte as snapshotted. If a future re-snapshot changes the minified
# variable names the anchor stops matching, and the app is served untouched
# rather than corrupted; SCENE_HOOK_OK records which happened.
# Anchored on r3f's render loop and its store hook rather than on any one
# component: the first runs every frame, the second on every r3f hook call, so
# the scene is published as soon as anything 3D is on screen. (An earlier
# attempt anchored on the wall-visibility component, which never mounts.)
SCENE_HOOKS = (
    ("render&&t.gl.render(t.scene,t.camera)",
     "render&&(window.__stScene=t.scene,window.__stGL=t.gl,t.gl.render(t.scene,t.camera))"),
    ('function JS(){const e=c.useContext(FS);if(!e)throw new Error("R3F: Hooks can only be used within the Canvas component!");return e}',
     'function JS(){const e=c.useContext(FS);if(!e)throw new Error("R3F: Hooks can only be used within the Canvas component!");return window.__stStore=e,e}'),
)
BUNDLE_NAME = "static/js/main.1d724872.js"

_bundle_cache = {}


def _hooked_bundle():
    """The main bundle with the scene published on `window.__stScene`."""
    if "body" not in _bundle_cache:
        path = os.path.join(WORKSPACE_DIR, BUNDLE_NAME)
        with open(path, encoding="utf-8") as handle:
            source = handle.read()
        installed = 0
        for anchor, patch in SCENE_HOOKS:
            if source.count(anchor) == 1:
                source = source.replace(anchor, patch)
                installed += 1
            else:
                app.logger.warning("scene hook anchor not unique/found: %.60s", anchor)
        _bundle_cache["body"] = source
        _bundle_cache["ok"] = installed == len(SCENE_HOOKS)
        app.logger.info("scene hooks installed: %d/%d", installed, len(SCENE_HOOKS))
    return _bundle_cache["body"], _bundle_cache["ok"]


@app.route("/workspace/")
@app.route("/workspace/<path:filename>")
def workspace_static(filename="index.html"):
    if filename.replace("\\", "/") == BUNDLE_NAME:
        body, ok = _hooked_bundle()
        response = app.response_class(body, mimetype="application/javascript")
        # The served bytes no longer match the file the URL is named after, and
        # the name carries the upstream build hash rather than ours, so a
        # year-long immutable cache would pin browsers to a pre-hook copy.
        # Revalidate instead: the ETag makes the steady state a 304.
        response.headers["Cache-Control"] = "no-cache"
        response.set_etag(hashlib.sha1(body.encode("utf-8")).hexdigest())
        response.headers["X-SecureTech-Scene-Hook"] = "ok" if ok else "missing"
        return response.make_conditional(request)

    # The bundle's own entry files change whenever the local adaptation does,
    # and they carry no content hash, so they must revalidate. The hashed
    # build output and the 3D assets keep the long cache.
    volatile = filename.endswith((".html", "local-adapter.js", "local-adapter.css",
                                  "manifest.json"))
    return send_from_directory(WORKSPACE_DIR, filename,
                               max_age=0 if volatile else 31536000)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
