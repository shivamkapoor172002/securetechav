# Content cleanup handoff

## Second review (11 September) — done

- **One master positioning.** *Professional AV & Technology Systems Integrator*, with the
  discipline line *AV | UC | Acoustics | Control | ICT | Lighting | Integration* beneath it.
  Applied to the homepage (Who We Are, page title, share text), About (heading, lead line, page
  title and share text), Contact title, and the corporate profile (cover, About slide, services
  heading — "Complete AV Consulting Services" is now "End-to-End AV & Technology Services").
  Metadata in `llms.txt`, `feed.xml` and `ai-plugin.json` follows. The earlier service-stage line
  (*AV Consulting | Design | … | AMC*) survives only as supporting prose.
- **Company figures, from the client.** 120+ Projects Delivered · 550+ Spaces Integrated · 18+
  Cities · 15+ Technology Partners. "550+ Enterprise Clients" was relabelled on About and in the
  profile — beside 120+ projects it could not also be clients. The stale *150+ clients / 200+
  projects* claims are gone from all eleven places they appeared (About ×3 meta, homepage and
  workspace share text, `llms.txt` ×3, `feed.xml` ×2, `ai-plugin.json`).
- **3D Designer promoted on the homepage** as a planning tool: *Design Your Space Before You
  Build It*, four numbered steps (choose your room → configure the AV → visualise the solution
  → generate your equipment list), *Launch 3D Designer*.
- **Industries in the main navigation**, on every page including the designer's own header, and
  a new `/Industries` page (`secure/templates/industries.html`) for the eight sectors: Corporate,
  Government, Education, Hospitality, Healthcare, Command & Control, Retail, Venues &
  Entertainment. Each links to Solutions and, where projects exist, straight to its sector on
  Case Studies (sector cards now carry anchors). The profile's Industries slide shows the same
  eight. Added to `sitemap.xml` and `llms.txt`.
- **Technology Partners line**: *We select technology based on application, performance,
  interoperability and lifecycle requirements.* — homepage and Case Studies.
- **Case studies restructured as engineering briefs** — Challenge / Solution / Scope — for MATS
  University, Patna University, ICAR-NIBSM and NIFT Varanasi. See the note below: only facts
  already on the site were used.
- The corporate profile PDF was regenerated from the updated deck.

## Needed from SecureTech to finish the case studies

The client asked for each project to read *Challenge → Solution (with the equipment) → Scope →
Result → Gallery*. The site holds only a description and a scope list per project, so the new
briefs carry **Challenge, Solution and Scope** built strictly from that existing copy.
**Result, equipment, and gallery were not written**: inventing speech-intelligibility gains or
brand lists for a named client would be exactly the kind of unsupported claim the review asked
to remove. Each card has a marked slot. For every project, please supply:

| Field | Example of what's needed |
|---|---|
| Challenge | What the client needed, in their terms |
| Equipment | Main systems and brands actually installed (e.g. DSP, microphones, displays, control) |
| Result | Measurable or observable outcome the client would confirm |
| Gallery | 3–6 real photos of the installed work |

Projects the review named that **have no case study at all yet**: ITC, Google, HCL, Taj, CBSE,
H&M, and the government townhalls. They appear as logos or sector-list entries only.

Also: three of the four case-study photos are placeholders (`IMAGE SLOT` comments in
`case_studies.html`), and the MATS photo is an event picture from the university's gallery that
does not show the installation.

## Decisions still needed

- **Healthcare and Command & Control have no projects on the site.** Their Industries cards link
  to Solutions and Contact instead. Add projects when there are some to show.
- **Houses of Worship** is not one of the eight industries, so it left the profile's Industries
  slide. Its projects are still listed under *Museums & Worship* on Case Studies.
- **The 3D Designer is promoted as a lead-generation tool, but opening a room still needs the
  administrator password.** Visitors can browse room types but cannot configure one. Decide
  whether visitors should get in, perhaps by leaving contact details instead of a password.
- Founding date (2020 in `llms.txt` vs August 2022 on About, alongside the separate 15+ years
  claim), headcount (30+ vs 50–100 in structured data), and the Google rating (4.9 / 51 on the
  page vs 5.0 / 29 in structured data, `llms.txt`, `feed.xml`, `ai-plugin.json`) are still
  unreconciled. Not guessed.
- Whether the new vision replaces both About visions and the deck vision.
- The full contact support paragraph, and expansion of abbreviated "SecureTech" names.
- Hospitality and Retail in the sector order, projects for Entertainment, and imagery for
  splitting Museum / House of Worship.
- Verify OEM certification, AVIXA and other compliance/standards claims before publication.

## Client flags from the first brief

- QSC versus QNC must be confirmed; three rail images still have generic Brand alternatives.
  Confirm logo permissions and reconcile the ten-brand metadata lists with the twenty-logo rail.
- Confirm ashish@ versus info@ addresses, the misspelled Instagram handle and conflicting
  Facebook/LinkedIn destinations.
- Legal links are placeholders; the footer navigation omits Case Studies, Industries and 3D
  Designer. Corporate Profile lacks metadata/language switching.
- Profile logos have duplicate asset copies; nested `secure/vercel.json` is stale; feed dates and
  room-capacity data need owner review.
- The misnamed unused `contactus.png` and obsolete `build_contact.py` remain untouched.
- Two Google reviews contain misspelled company names. Their original wording is preserved.

## About hero provenance

Asset: `secure/static/aboutus.webp`. Generated with an image tool at 1448 × 1086 and upscaled to
2560 × 1920 — a native-resolution replacement would be sharper. Alt text identifies an
illustrative room rather than claiming it is a completed client project.
