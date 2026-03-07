#!/usr/bin/env python3
"""
SecureTech AV Designs — HTML Presentation → PDF Converter
Uses Playwright (Chromium) for pixel-perfect CSS rendering.

Usage:
    python3 convert_to_pdf.py
    python3 convert_to_pdf.py --input path/to/your.html --output output.pdf

Requirements:
    pip install playwright
    playwright install chromium
"""

import argparse
import os
import sys
import time
from pathlib import Path


def convert_html_to_pdf(html_path: str, output_pdf: str) -> bool:
    """Convert an HTML presentation file to a multi-page PDF."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌  Playwright is not installed.")
        print("    Run:  pip install playwright && playwright install chromium")
        return False

    html_path = Path(html_path).resolve()
    if not html_path.exists():
        print(f"❌  HTML file not found: {html_path}")
        return False

    output_pdf = Path(output_pdf).resolve()
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    # Slide dimensions from CSS:  338.67 mm × 190.5 mm  (widescreen 16:9)
    PAGE_WIDTH_MM  = 338.67
    PAGE_HEIGHT_MM = 190.5

    print(f"📄  Source  : {html_path}")
    print(f"📁  Output  : {output_pdf}")
    print(f"📐  Page    : {PAGE_WIDTH_MM} mm × {PAGE_HEIGHT_MM} mm (landscape 16:9)")
    print()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--font-render-hinting=none",   # crisper web fonts
            ],
        )

        page = browser.new_page(
            viewport={"width": 1280, "height": 720},
        )

        # ── Load the HTML file ──────────────────────────────────────────────
        file_url = html_path.as_uri()
        print(f"🌐  Loading {file_url} …")
        page.goto(file_url, wait_until="networkidle", timeout=60_000)

        # Wait for web fonts (Google Fonts) and any lazy images
        time.sleep(2)

        # Ensure all images are loaded (or failed gracefully)
        page.evaluate("""() => {
            return new Promise(resolve => {
                const imgs = Array.from(document.images);
                if (imgs.length === 0) return resolve();
                let pending = imgs.length;
                const done = () => { if (--pending === 0) resolve(); };
                imgs.forEach(img => {
                    if (img.complete) { done(); }
                    else {
                        img.addEventListener('load',  done);
                        img.addEventListener('error', done);
                    }
                });
            });
        }""")

        # ── Count slides ────────────────────────────────────────────────────
        slide_count = page.evaluate("document.querySelectorAll('.slide').length")
        print(f"🎞️   Detected {slide_count} slide(s)")

        # ── PDF generation ──────────────────────────────────────────────────
        print("🖨️   Rendering PDF …")
        pdf_bytes = page.pdf(
            format=None,                   # use explicit width/height
            width=f"{PAGE_WIDTH_MM}mm",
            height=f"{PAGE_HEIGHT_MM}mm",
            print_background=True,         # ← keeps gradients, colours, BG images
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,     # respect @page rule in CSS
        )

        browser.close()

    # ── Write output ────────────────────────────────────────────────────────
    with open(output_pdf, "wb") as fh:
        fh.write(pdf_bytes)

    size_kb = output_pdf.stat().st_size / 1024
    print(f"\n✅  Done!  →  {output_pdf}  ({size_kb:.0f} KB)")
    return True


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert SecureTech AV HTML presentation to PDF"
    )
    parser.add_argument(
        "--input", "-i",
        default="index.html",
        help="Path to the HTML file  (default: index.html)",
    )
    parser.add_argument(
        "--output", "-o",
        default="SecureTech_AV_Corporate_Profile.pdf",
        help="Output PDF filename  (default: SecureTech_AV_Corporate_Profile.pdf)",
    )
    args = parser.parse_args()

    success = convert_html_to_pdf(args.input, args.output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()