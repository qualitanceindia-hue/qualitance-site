# Splits the certifications guide into one page per scheme (one keyword per URL), rebuilds the hub, and regenerates sitemap.xml.
import re, json, html, os, shutil, glob
H = html.escape
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = "https://qualitanceindia.in"
src = "tools/certifications.source.html"
if not os.path.exists(src): shutil.copy("certifications.html", src)
doc = open(src, encoding="utf-8").read()
style = re.search(r"<style>.*?</style>", doc, re.S).group(0)
fonts = re.search(r'<link rel="preconnect" href="https://fonts.googleapis.com">.*?rel="stylesheet">', doc, re.S).group(0)
header = re.search(r"<header>.*?</header>", doc, re.S).group(0)
footer = re.search(r"<footer>.*?</footer>", doc, re.S).group(0)
EXTRA = r'<style>.crumb{font-size:14px;color:var(--muted);margin:0 0 16px}.crumb a{color:inherit}details{border-top:1px solid var(--line);padding:16px 0}summary{cursor:pointer;font-weight:600;list-style:none;display:flex;justify-content:space-between;gap:16px}summary::-webkit-details-marker{display:none}summary::after{content:"+";font-size:22px}details[open] summary::after{content:"\2212"}details p{margin:10px 0 0;color:var(--muted)}.rl a{display:block;margin-bottom:8px}</style>'
SERV = [
("isi", "isi-mark-certification.html", "ISI Mark certification (BIS Scheme-I)",
 "ISI Mark Certification: Procedure, Documents and Timeline | Qualitance India",
 "How to get the ISI Mark under BIS Scheme-I, for mandatory (QCO) and voluntary products: step-by-step procedure, documents required and indicative timeline.",
 "For Indian factories. Covers mandatory certification under a QCO and voluntary certification, with the procedure, documents and timeline.",
 [("What is the difference between mandatory and voluntary ISI certification?", "Mandatory certification applies to products covered by a QCO, which cannot be made, imported or sold without the mark. Voluntary certification applies where an Indian Standard exists but no QCO does. The application process is the same."),
  ("Does BIS inspect my factory for the ISI Mark?", "Yes. Under Scheme-I a BIS officer inspects the factory and draws samples for testing before the licence is granted."),
  ("Is one licence enough for all my products?", "A licence is granted against specific products and Indian Standards, so every product line must be covered by it. We check the scope before you apply.")]),
("fmcs", "fmcs-bis-certification.html", "FMCS: BIS certification for foreign manufacturers",
 "FMCS BIS Certification for Foreign Manufacturers: Process and Documents | Qualitance India",
 "BIS Foreign Manufacturers Certification Scheme (FMCS): how overseas factories get the ISI Mark, the Authorised Indian Representative role, documents and timeline.",
 "For factories outside India that export QCO-covered products to India. Covers the AIR role, overseas inspection, documents and timeline.",
 [("Who applies under FMCS?", "The overseas manufacturer applies, through an Authorised Indian Representative who lives in India and handles all communication with BIS."),
  ("Does BIS visit factories outside India?", "Yes. BIS officers inspect the overseas factory as part of the process, and samples are tested."),
  ("Is FMCS different from the ISI Mark?", "The mark is the same. FMCS is Scheme-I applied to factories outside India, with the Authorised Indian Representative requirement and an overseas inspection.")]),
("crs", "bis-crs-registration.html", "BIS CRS registration (Compulsory Registration Scheme)",
 "BIS CRS Registration: Procedure, Documents and Timeline | Qualitance India",
 "How to get BIS CRS registration for electronics and IT products: step-by-step procedure, documents required, test report validity and indicative timeline.",
 "For notified electronics and IT products. Covers the procedure, laboratory testing, documents and timeline.",
 [("Does CRS need a factory inspection?", "No. CRS registration is based on laboratory testing of samples, but the registration is granted to the factory."),
  ("How long is a CRS test report valid?", "Apply within 90 days of the test report date."),
  ("How long does a CRS registration last?", "Two years, and it can be renewed.")]),
]
def sec(i): return re.search(r'<section class="scheme" id="%s">.*?</section>' % i, doc, re.S).group(0)
def shell(title, desc, canon, ld, body):
    return ('<!doctype html><html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
      '<title>%s</title><meta name="description" content="%s"><link rel="canonical" href="%s/%s">%s<link rel="stylesheet" href="site.css">%s%s'
      '<script type="application/ld+json">%s</script></head><body>%s<main>%s</main>%s</body></html>') % (H(title), H(desc), SITE, canon, fonts, style, EXTRA, json.dumps(ld), header, body, footer)
hub = doc
for k, (i, page, name, title, desc, lede, faqs) in enumerate(SERV):
    full = sec(i)
    others = [s for s in SERV if s[0] != i]
    fq = "".join("<details><summary>%s</summary><p>%s</p></details>" % (H(q), H(a)) for q, a in faqs)
    rl = "".join('<a href="%s">%s</a>' % (o[1], o[2]) for o in others) + '<a href="locations.html">BIS consultants by city</a><a href="book.html">Book a video call</a>'
    body = ('<div class="wrap page"><p class="crumb"><a href="index.html">Home</a> / <a href="certifications.html">Certifications</a> / %s</p><h1>%s</h1><p class="lede">%s</p>'
            '<p style="margin-top:24px"><a class="btn" href="book.html">Book a video call</a></p>%s'
            '<section class="scheme"><div><h2>Common questions</h2></div><div>%s</div></section>'
            '<section class="scheme"><div><h2>Related</h2></div><div class="rl">%s</div></section></div>') % (H(name), H(name), H(lede), full, fq, rl)
    ld = {"@context": "https://schema.org", "@graph": [
      {"@type": "Service", "name": name, "serviceType": "BIS certification consulting", "provider": {"@type": "ProfessionalService", "name": "Qualitance India", "url": SITE + "/"}, "areaServed": ["IN", "Worldwide"]},
      {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Certifications", "item": SITE + "/certifications.html"}, {"@type": "ListItem", "position": 3, "name": name}]},
      {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]}
    open(page, "w", encoding="utf-8").write(shell(title, desc, page, ld, body))
    left = full.split("</div><div>\n<h3>Procedure</h3>")[0]
    summary = left + '</div><div><p>Step-by-step procedure, indicative timeline and the full documents checklist.</p><p><a class="btn" href="%s">Read the full guide</a></p></div></section>' % page
    hub = hub.replace(full, summary)
open("certifications.html", "w", encoding="utf-8").write(hub)
# sitemap from every html page in the folder
pages = sorted(glob.glob("*.html"), key=lambda p: (p != "index.html", p))
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join("  <url><loc>%s/%s</loc><lastmod>2026-10-09</lastmod></url>\n" % (SITE, "" if p == "index.html" else p) for p in pages) + "</urlset>\n")
print("services built; sitemap pages:", len(pages))
