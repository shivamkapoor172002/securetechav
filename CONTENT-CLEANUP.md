# Content cleanup handoff

Questions for the client are in **[CLIENT-QUESTIONS.md](CLIENT-QUESTIONS.md)** — send that as it is.

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
  projects* claims are gone from all eleven places they appeared.
- **3D Designer promoted on the homepage** as a planning tool: *Design Your Space Before You
  Build It*, four numbered steps, *Launch 3D Designer*.
- **Industries in the main navigation**, on every page including the designer's own header, and
  a new `/Industries` page (`secure/templates/industries.html`) for the eight sectors. Each links
  to Solutions and, where projects exist, straight to its sector on Case Studies. The profile's
  Industries slide shows the same eight. Added to `sitemap.xml` and `llms.txt`.
- **Technology Partners line**: *We select technology based on application, performance,
  interoperability and lifecycle requirements.* — homepage and Case Studies.
- **Case studies restructured as engineering briefs** — Challenge / Solution / Scope — built
  strictly from what the site already said about each project.
- **No stand-in photos on case studies.** None of the four featured projects had a photo of the
  installed work (three were stand-ins, MATS was a university event picture), so the cards are
  text-only until real photos arrive. Each card marks where a photo goes back.
- The corporate profile PDF was regenerated from the updated deck.

## Decided

- **The 3D Designer keeps its password.** Visitors browse the room types; opening a room in the
  configurator needs the administrator password.
- **Company facts the client did not mention stay as they are** — founding date, headcount and
  Google rating are unchanged and go to the client as questions, not edits.

## Waiting on the client (all in CLIENT-QUESTIONS.md)

- Case studies: challenge, equipment, result, photos and naming permission per project, for the
  four on the site and for ITC, Google, HCL, Taj, CBSE, H&M and the townhall projects.
- Projects for Healthcare and Command & Control; Houses of Worship leaving the Industries list.
- Sector order on Case Studies (Hospitality, Retail, Entertainment, Museum / Worship split).
- Founding date (2020 vs August 2022, plus the 15+ years line), headcount (30+ vs 50–100), and
  Google rating (4.9 / 51 on the page vs 5.0 / 29 in structured data, `llms.txt`, `feed.xml`,
  `ai-plugin.json`).
- Vision statement; certifications and standards claims; QSC vs QNC; the three unnamed logos and
  logo permissions; ashish@ vs info@; social links; legal pages; the contact paragraph.
- A real photo for the About banner.

## Housekeeping not waiting on anyone

- The footer navigation omits Case Studies, Industries and 3D Designer. Corporate Profile lacks
  metadata and language switching.
- Profile logos have duplicate asset copies; nested `secure/vercel.json` is stale; feed dates and
  room-capacity data need owner review.
- The misnamed unused `contactus.png` and obsolete `build_contact.py` remain untouched.
- Two Google reviews contain misspelled company names. Their original wording is preserved.

## About hero provenance

Asset: `secure/static/aboutus.webp`. Generated with an image tool at 1448 × 1086 and upscaled to
2560 × 1920. Alt text identifies an illustrative room rather than claiming it is a completed
client project. A real photo from the client would replace it.
