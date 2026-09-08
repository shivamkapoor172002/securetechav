#!/usr/bin/env python
"""Regenerate secure/static/securetech_profile.pdf from the live deck.

The corporate profile exists twice: as the HTML deck at /CorporateProfile and as
a downloadable PDF linked from six places across the site. The PDF is a static
file, so editing the deck does nothing for it — the two drift apart silently, and
have done before (the deck was at 22 slides while the PDF was still shipping 26
pages from six months earlier).

Run this after any edit to secure/templates/securetech_profile.html.

    python scripts/export_profile.py

It renders each .slide at its authored 1280x720 and then re-encodes the embedded
images, which is where the weight is: a straight Chromium print of this deck runs
to about 40 MB because the slide backgrounds embed as lossless streams.
Re-encoding is lossy — that is the trade for a file people will actually
download — so QUALITY is deliberately conservative and the script reports what it
did rather than compressing silently.

Requires: playwright (with chromium, or a local Chrome) and pymupdf.
    pip install playwright pymupdf && playwright install chromium
"""

from __future__ import annotations

import io
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
APP = REPO / "secure" / "app.py"
OUT = REPO / "secure" / "static" / "securetech_profile.pdf"
URL = "http://127.0.0.1:5000/CorporateProfile"

SLIDE_W, SLIDE_H = 1280, 720          # the deck's authored slide box
QUALITY = 72                           # JPEG quality for re-encoded image streams
MIN_BYTES = 60_000                     # leave small images (logos, icons) alone


def serving() -> bool:
    import urllib.error
    import urllib.request
    try:
        urllib.request.urlopen("http://127.0.0.1:5000/", timeout=3)
        return True
    except (urllib.error.URLError, OSError):
        return False


def render(path: Path) -> None:
    """Print the deck to PDF, one page per slide."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch()
        except Exception:
            # No downloaded chromium; fall back to an installed Chrome.
            browser = pw.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": SLIDE_W, "height": SLIDE_H})
        page.goto(URL, wait_until="networkidle", timeout=90_000)
        page.wait_for_timeout(2500)          # webfonts and the deck's scale script
        slides = page.locator(".slide").count()
        page.pdf(
            path=str(path),
            width=f"{SLIDE_W}px",
            height=f"{SLIDE_H}px",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()
    print(f"  rendered {slides} slides")


def compress(path: Path) -> tuple[int, int]:
    """Re-encode large embedded images as JPEG. Returns (touched, skipped)."""
    import fitz
    from PIL import Image

    doc = fitz.open(path)
    touched = skipped = 0
    seen: set[int] = set()

    for page in doc:
        for info in page.get_images(full=True):
            xref = info[0]
            if xref in seen:
                continue
            seen.add(xref)
            raw = doc.extract_image(xref)
            data = raw["image"]
            if len(data) < MIN_BYTES:
                skipped += 1
                continue
            try:
                im = Image.open(io.BytesIO(data))
                # An image with real transparency must keep its alpha, so it is
                # left as it is rather than flattened onto a guessed background.
                if im.mode in ("RGBA", "LA", "P") and "transparency" in im.info:
                    skipped += 1
                    continue
                im = im.convert("RGB")
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=QUALITY, optimize=True,
                        progressive=True)
                if buf.tell() < len(data):
                    # compress=False matters: the default re-deflates the bytes,
                    # which would leave a zlib stream declared as /DCTDecode and
                    # every re-encoded image unreadable.
                    doc.update_stream(xref, buf.getvalue(), new=True,
                                      compress=False)
                    doc.xref_set_key(xref, "Filter", "/DCTDecode")
                    doc.xref_set_key(xref, "ColorSpace", "/DeviceRGB")
                    doc.xref_set_key(xref, "BitsPerComponent", "8")
                    touched += 1
                else:
                    skipped += 1
            except Exception:
                skipped += 1

    tmp = path.with_suffix(".tmp.pdf")
    doc.save(tmp, garbage=4, deflate=True, clean=True)
    doc.close()
    os.replace(tmp, path)
    return touched, skipped


def main() -> int:
    started = None
    if not serving():
        print("Flask is not running; starting it")
        started = subprocess.Popen([sys.executable, "app.py"],
                                   cwd=str(APP.parent),
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
        for _ in range(40):
            time.sleep(0.5)
            if serving():
                break
        else:
            print("could not reach http://127.0.0.1:5000/", file=sys.stderr)
            started.terminate()
            return 1

    before = OUT.stat().st_size if OUT.exists() else 0
    try:
        print(f"rendering {URL}")
        render(OUT)
        raw = OUT.stat().st_size
        print(f"  raw          {raw:,} bytes")

        print("compressing embedded images")
        touched, skipped = compress(OUT)
        final = OUT.stat().st_size
        print(f"  re-encoded   {touched} images, left {skipped} alone")

        import fitz
        with fitz.open(OUT) as doc:
            pages = doc.page_count
        print()
        print(f"{OUT.relative_to(REPO)}")
        print(f"  {pages} pages, {final:,} bytes ({final / 1e6:.1f} MB)")
        if before:
            print(f"  was {before:,} bytes ({before / 1e6:.1f} MB)")
    finally:
        if started:
            started.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
