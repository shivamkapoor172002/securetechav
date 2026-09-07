# Content cleanup handoff

Implemented the supplied headline and Who We Are copy, case-study and contact hero copy, legal-name corrections, integrator positioning, selected-client and technology headings, Audio-Visual and Architectural Lighting terminology, maroon solutions accent, real structured-data telephone, cache-versioned backgrounds, and accurate OG image dimensions. Customer reviews, external handles, filenames, and the sector grid were preserved.

Removed Flagship Projects and Appendix / Technical Annex from the corporate deck. The downloadable PDF is regenerated from the resulting 20-slide HTML. Print navigation is hidden.

Validation: all seven public routes returned HTTP 200 at 1440px and 390px, with no horizontal overflow or broken images. Browser checks loaded the site's fonts and styles; translation/analytics and video requests were suppressed. The authenticated workspace route, rendered background cache versions, JSON-LD, well-known JSON, feed XML, unchanged review array and git whitespace checks passed. The final PDF is 13,289,843 bytes (about 13.3 MB), has 20 nonempty pages, excludes both removed slide titles, and all pages render successfully. Compression changes embedded image streams while preserving text and vector drawing resources.

## Decisions still needed

- Confirm clients/projects: body 550+/120+ versus metadata 150+/200+. Update all affected metadata and both count-up attributes together once confirmed.
- Confirm founding date (2020 versus August 2022, with a separate 15+ years claim), headcount (30+ versus 50–100), and Google rating/reviews (4.9/51 versus 5.0/29). These have not been guessed or reconciled.
- Decide whether the supplied new vision replaces both About visions and the deck vision. Existing vision statements remain pending that decision.
- Confirm replacement of the full contact support paragraph and expansion of abbreviated SecureTech names. Those ambiguous locations remain.
- Decide treatment of Hospitality and Retail, the projects for Entertainment, whether Venues becomes Government, and imagery for splitting Museum / House of Worship. Sector cards remain unchanged.
- Verify OEM certification, AVIXA and other compliance/standards claims before publication. The unsupported independence language was replaced with integration delivery language; this does not verify certifications.

## Client flags from the brief

- QSC versus QNC must be confirmed; three rail images still have generic Brand alternatives. Confirm logo permissions and reconcile the ten-brand metadata lists with the twenty-logo rail.
- Confirm ashish@ versus info@ addresses, the misspelled Instagram handle and conflicting Facebook/LinkedIn destinations.
- Legal links are placeholders; footer navigation omits Case Studies and 3D Designer. Corporate Profile lacks metadata/language switching. These were flagged rather than silently changed.
- Profile logos have duplicate asset copies; nested vercel.json is stale; sitemap routes and dates, feed dates and room-capacity data need owner review.
- The misnamed unused contactus.png and obsolete build_contact.py remain untouched. Solution tile compression was conditional in the brief and remains a separate optimization.
- Two Google reviews contain misspelled company names. Their original wording was preserved exactly. The profile testimonial was also preserved.
- Architectural Lighting now sits alongside Architectural Acoustics, as requested. The equivalent Lighting Architecture phrasing was normalized for consistency; image filenames remain unchanged.

## About hero provenance

Asset: `secure/static/aboutus.webp`. Generated with the built-in imagegen tool, then converted to WebP at 2560 × 1920. The tool returned 1448 × 1086, so the saved version is upscaled. Alt text identifies an illustrative room rather than claiming it is a completed client project.

Prompt: Generate a photorealistic architectural interior photograph for an About page hero. Landscape 2560×1920, 4:3. A modern AV control and integration environment: a large commissioned boardroom seen wide, walnut and oak architectural accents, ivory and charcoal furnishings, large wall displays showing abstract non-readable content, ceiling-mounted speakers and cameras visible, clean white ceiling with linear recessed lighting, restrained greenery. Bright natural daylight, high contrast, refined realistic materials, professional architectural photography, eye-level composition with subject centred and edges uncluttered and safe to crop 5% on every side. Empty room, no people, no website UI, no watermarks, no readable text. Will be displayed at opacity 0.55 over black.
