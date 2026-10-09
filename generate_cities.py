# Generates one SEO page per city plus locations.html. Run from the site folder: python3 tools/generate_cities.py
# To add a city: append one entry to CITIES. Write real local content: pages that only swap the city name will not rank.
import json, html, os
SITE = "https://qualitanceindia.in"
H = html.escape
# slug, name, areas, intro, [(what you make, what it usually needs)], BIS office note, [(question, answer)]
CITIES = [
("delhi","Delhi","Okhla, Mayapuri, Wazirpur, Bawana, Narela",
 "Delhi's industrial areas run thousands of small and mid-size units in electrical goods, LED lighting, plastics, garments and light engineering. Many of them first meet BIS when a buyer, marketplace or customs officer asks for proof of certification.",
 [("LED and electrical goods","ISI Mark or CRS, depending on the exact product"),("Household appliances","IS 302 series under ISI"),("Plastic and kitchenware","Check the current QCO for each item"),("Electronic accessories","CRS registration, often with an Authorised Indian Representative for imported brands")],
 "BIS headquarters, Manak Bhavan, is in New Delhi. Our office is in Noida, close to Delhi, so Delhi clients can visit us.",
 [("Do small units in Okhla or Mayapuri need BIS certification?","Only if the product is covered by a QCO, or if you choose voluntary certification. Unit size does not exempt a product, though some QCOs give small enterprises extra time. Check the notification for your product.")]),
("noida","Noida","Noida, Greater Noida, Sector 63, Phase 2",
 "Noida and Greater Noida host many electronics makers, mobile phone assemblers and IT hardware brands. For most of them the question is not whether they need BIS, but which registration covers each model and who files it.",
 [("Mobile phones and smart watches","CRS under IS 13252 (Part 1)"),("Power adapters, chargers and power banks","CRS registration"),("Laptops, tablets and printers","CRS registration"),("Contract manufacturing for brands","Aligned documents between factory and brand owner")],
 "BIS added a Noida branch office when it reorganised its branch network in 2021. Our own office is in Sector 3, Noida.",
 [("Do I need CRS registration for chargers and power banks made in Noida?","Power adapters and power banks appear in the CRS list under IS 13252 (Part 1). We confirm the current category and standard for your model before you send samples for testing.")]),
("gurugram","Gurugram","Gurugram, IMT Manesar, Bawal",
 "Gurugram and the Manesar belt are known for automotive components, electronics assembly and export-oriented manufacturing. The compliance route differs sharply between a component supplier and a consumer product brand.",
 [("Automotive components","Often AIS type approval rather than ISI"),("Electronics assembly","CRS for notified products"),("Appliances and electrical products","ISI under the relevant QCO"),("Importers and distributors","Checking the supplier's registration before shipment")],
 "BIS has a branch office in nearby Faridabad. Filing is online, so the office location rarely matters.",
 [("Does an auto component maker in Manesar need BIS?","Many auto components follow Automotive Industry Standards (AIS) approval rather than the ISI Mark. Which applies depends on the component, so we check both routes.")]),
("mumbai","Mumbai","Andheri MIDC, Thane, Navi Mumbai, Taloja",
 "Mumbai, Thane and Navi Mumbai combine chemicals, electrical equipment, packaging and plastics manufacturers with a large importer base clearing goods through the Nhava Sheva port. Importers here usually need answers before a shipment is booked.",
 [("Importers via Nhava Sheva","Confirm QCO coverage and the manufacturer's licence before shipping"),("Electrical equipment","ISI Mark under the relevant standard"),("Chemicals and polymers","Several orders were withdrawn in late 2025, so status needs checking"),("Packaged goods","Legal Metrology (LMPC) declarations")],
 "The BIS Western Regional Office is at MIDC, Andheri (East), Mumbai.",
 [("I import through Nhava Sheva. When should BIS be sorted?","Before the shipment is booked. A product covered by a QCO cannot be cleared without the required mark, so confirm the certification and the overseas manufacturer's registration first.")]),
("pune","Pune","Pimpri-Chinchwad, Chakan, Ranjangaon, Talegaon",
 "Pune's Pimpri-Chinchwad, Chakan and Ranjangaon belts are built around automotive and engineering supply chains, with machine tools and electronics alongside. Suppliers here deal with several approval systems at once.",
 [("Automotive components","AIS approvals, sometimes with ISI for specific items"),("Machine tools and engineering goods","Check the current machinery-related orders, which have changed"),("Electronics","CRS for notified products"),("Electrical accessories","ISI Mark under the relevant standard")],
 "The BIS Pune Branch Office is at the MIDC Building, Market Yard, Gultekdi.",
 [("Is AIS the same as BIS ISI?","No. AIS are Automotive Industry Standards used for vehicle and component approval, while the ISI Mark is BIS's product certification mark. A component may need one, the other or neither.")]),
("ahmedabad","Ahmedabad","Naroda, Vatva, Odhav, Changodar, Sanand",
 "Ahmedabad's industrial estates cover chemicals, pharmaceuticals, textiles, plastics and engineering, with automotive supply chains around Sanand. Many chemical and textile-input QCOs have changed recently, which makes a status check essential.",
 [("Chemicals and polymers","Several QCOs were withdrawn in late 2025; confirm product by product"),("Plastics and packaging","Check the current QCO and Legal Metrology rules"),("Engineering goods","ISI where a QCO applies"),("Exporters","Buyer-driven voluntary certification")],
 "The BIS Ahmedabad Branch Office is near Ashram Road.",
 [("Several chemical QCOs were withdrawn. Do chemical units here still need BIS?","Many orders for chemicals and polymers were withdrawn in late 2025, so many products no longer mandate it. Certification can still be voluntary or demanded by buyers. Check product by product.")]),
("surat","Surat","Pandesara, Sachin, Udhna, Kadodara",
 "Surat is a textile, synthetic yarn and diamond city, with chemicals and engineering around Pandesara and Sachin. Compliance questions here split between textile inputs, which have seen order changes, and jewellery hallmarking.",
 [("Synthetic yarn and fibre","Several textile-input QCOs were withdrawn in 2025; confirm current status"),("Gold jewellery","BIS hallmarking registration and HUID"),("Chemicals and dyes","Check the current QCO list"),("Machinery","Check current machinery-related orders")],
 "BIS added a Surat branch office when it reorganised its branch network in 2021.",
 [("Do jewellers in Surat need hallmarking?","Gold jewellery hallmarking with HUID is mandatory for jewellers in notified districts, and it needs BIS registration. We help with registration and check that your district is covered.")]),
("chennai","Chennai","Sriperumbudur, Oragadam, Ambattur, Maraimalai Nagar",
 "Chennai and the Sriperumbudur-Oragadam belt are centres for automotive, electronics and heavy engineering, and the city's port serves a large importer base. Electronics contract manufacturers are often the busiest clients for registration work.",
 [("Electronics assembly","CRS registration, granted to the factory"),("Automotive components","AIS approvals"),("Importers via Chennai port","QCO checks before shipment"),("Electrical products","ISI Mark under the relevant standard")],
 "The BIS Southern Regional Office is at the C.I.T. Campus, Chennai.",
 [("Do electronics assembled near Chennai need CRS registration?","Notified electronics and IT products do, and the registration is granted to the factory. Contract manufacturers and brand owners need aligned documents, including matching names and model numbers.")]),
("coimbatore","Coimbatore","Kurichi, Peelamedu, Ganapathy, Sulur",
 "Coimbatore is known for pumps and motors, textile machinery, foundries, wet grinders and electrical switchgear, mostly in small and medium units. Many are family-run and have never handled a BIS audit before.",
 [("Pumps and motors","ISI depends on the product and current QCO; BEE labelling may also apply"),("Wet grinders and kitchen appliances","IS 302 series under ISI, where covered"),("Electrical switchgear","Check current electrical-equipment orders"),("Foundry castings","Mostly buyer-driven standards")],
 "The BIS Coimbatore Branch Office is on Race Course Road.",
 [("Do pump and motor makers in Coimbatore need ISI?","It depends on the product and the current QCO. We check the Indian Standard for your exact pump or motor, and whether BEE energy labelling also applies.")]),
("ludhiana","Ludhiana","Focal Point, Industrial Area A and B, Sherpur",
 "Ludhiana is one of India's densest small-industry clusters: bicycles and parts, hosiery, auto components, hand tools, sewing machines and machine tools. Most units are exporters or suppliers to larger brands, so certification is often triggered by a buyer.",
 [("Bicycle parts and auto components","Check ISI and AIS routes for each part"),("Hand tools","A new QCO has been reported; confirm the notification and date"),("Machine tools and sewing machines","Check current machinery-related orders"),("Hosiery and knitwear","Mostly buyer standards; BIS rarely applies")],
 "Ludhiana falls under the jurisdiction of the BIS Northern Regional Office in Chandigarh.",
 [("Do hand tool makers in Ludhiana need BIS?","A new QCO for hand tools has been reported for 2026. Confirm the notification and effective date for your tool before you plan production or imports.")]),
("rajkot","Rajkot","Aji GIDC, Shapar-Veraval, Metoda, Bhaktinagar",
 "Rajkot's engineering cluster covers diesel engines, pumps, bearings, forgings, castings and machine tools, with hundreds of small suppliers. Many sell into larger OEMs that now ask for certified components.",
 [("Diesel engines and pumps","Check ISI and BEE routes for each product"),("Machine tools and forgings","Check current machinery-related orders"),("Auto components","AIS or ISI, depending on the part"),("Kitchenware and metal products","Check the current QCO for each item")],
 "The BIS Rajkot Branch Office is on Kalawad Road.",
 [("Which BIS office handles Rajkot?","The Rajkot Branch Office on Kalawad Road. Applications are filed online, so you can work with us from your factory without travelling.")]),
]
GENERIC = ("Do I need to be in {n} to work with Qualitance India?",
 "No. Our office is in Noida, and BIS applications are filed online. We work with {n} manufacturers through video calls and handle documents remotely.")
CSS = """<style>
.lc{display:grid;grid-template-columns:1fr 2fr;gap:56px;padding:56px 0;border-top:1px solid var(--line)}
.lc h2{font-size:clamp(26px,3vw,34px)}.lc p{color:var(--muted);margin:0 0 14px}
dl.k{margin:0}dl.k div{display:grid;grid-template-columns:240px 1fr;gap:16px;padding:12px 0;border-top:1px solid var(--line)}dl.k dt{font-weight:600}dl.k dd{margin:0;color:var(--muted)}
details{border-top:1px solid var(--line);padding:16px 0}summary{cursor:pointer;font-weight:600;list-style:none;display:flex;justify-content:space-between;gap:16px}
summary::-webkit-details-marker{display:none}summary::after{content:"+";font-size:22px;line-height:1}details[open] summary::after{content:"\\2212"}
details p{margin:10px 0 0;color:var(--muted);max-width:44em}.rel a{display:inline-block;margin:0 16px 8px 0}
.cta{background:var(--ink);color:#fff;padding:40px;margin-top:24px}.cta p{color:#B9C8D1;margin:8px 0 20px}.cta .btn{background:#fff;color:var(--ink)}
@media(max-width:860px){.lc{grid-template-columns:1fr;gap:20px}dl.k div{grid-template-columns:1fr;gap:2px}}</style>"""
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Public+Sans:wght@400;500;600&display=swap" rel="stylesheet">'
NAV = '<header><div class="wrap bar"><a class="brand" href="index.html">Qualitance India</a><nav aria-label="Main"><a href="certifications.html">Certifications</a><a href="locations.html">Locations</a><a href="index.html#faq">FAQ</a><a href="index.html#contact">Contact</a><a class="btn" href="book.html">Book a video call</a></nav></div></header>'
FOOT = '<footer><div class="wrap">&copy; 2026 Qualitance India. Information on this site is for guidance and is not legal advice.</div></footer>'
def url(c): return "bis-certification-consultant-%s.html" % c[0]
def shell(title, desc, canon, ld, body):
    return ('<!doctype html><html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
      '<title>%s</title><meta name="description" content="%s"><link rel="canonical" href="%s/%s">%s<link rel="stylesheet" href="site.css">%s'
      '<script type="application/ld+json">%s</script></head><body>%s<main>%s</main>%s</body></html>') % (H(title),H(desc),SITE,canon,FONTS,CSS,json.dumps(ld),NAV,body,FOOT)
def city_page(i):
    c = CITIES[i]; slug,n,areas,intro,cl,office,faq = c
    faqs = faq + [(GENERIC[0].format(n=n), GENERIC[1].format(n=n))]
    rel = [CITIES[(i+k)%len(CITIES)] for k in (1,2,3,4)]
    dl = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (H(a),H(b)) for a,b in cl)
    fq = "".join("<details><summary>%s</summary><p>%s</p></details>" % (H(q),H(a)) for q,a in faqs)
    rl = "".join('<a href="%s">BIS consultant in %s</a>' % (url(r),r[1]) for r in rel)
    body = ('<div class="wrap page"><h1>BIS certification consultant in %s</h1><p class="lede">%s</p>'
     '<p style="margin-top:24px"><a class="btn" href="book.html">Book a video call</a></p>'
     '<section class="lc"><div><h2>What %s manufacturers ask us about</h2><p>Units in %s and nearby areas.</p></div><dl class="k">%s</dl></section>'
     '<section class="lc"><div><h2>BIS offices and filing</h2></div><div><p>%s</p><p>Applications and registrations are filed online. See how each route works: <a href="certifications.html#isi">ISI Mark</a>, <a href="certifications.html#fmcs">FMCS for overseas factories</a> and <a href="certifications.html#crs">CRS</a>.</p></div></section>'
     '<section class="lc"><div><h2>Questions from %s</h2></div><div>%s</div></section>'
     '<div class="cta"><h2>Tell us what you make or import in %s</h2><p>A 30-minute video call to confirm which approvals apply, the documents you need and a realistic timeline.</p><a class="btn" href="book.html">Book a video call</a></div>'
     '<section class="lc rel"><div><h2>Other cities</h2></div><div>%s<a href="locations.html">All locations</a></div></section></div>') % (n,H(intro),n,H(areas),dl,H(office),n,fq,n,rl)
    ld = {"@context":"https://schema.org","@graph":[
      {"@type":"Service","name":"BIS certification consulting in %s" % n,"provider":{"@type":"ProfessionalService","name":"Qualitance India","url":SITE+"/"},"areaServed":{"@type":"City","name":n},"serviceType":"BIS ISI, FMCS and CRS certification consulting"},
      {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Locations","item":SITE+"/locations.html"},{"@type":"ListItem","position":3,"name":n}]},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}]}
    return url(c), shell("BIS Certification Consultant in %s | ISI, CRS, FMCS | Qualitance India" % n,
      "BIS certification consultant for %s manufacturers and importers. ISI Mark, CRS and FMCS approvals through video consultation and online filing. Book a call." % n, url(c), ld, body)
files = dict(city_page(i) for i in range(len(CITIES)))
items = "".join('<li><a href="%s">BIS certification consultant in %s</a></li>' % (url(c),c[1]) for c in CITIES)
files["locations.html"] = shell("BIS Certification Consultant by City | Qualitance India",
  "Cities we support for BIS ISI, CRS and FMCS certification, including Delhi, Noida, Mumbai, Pune, Ahmedabad, Chennai, Coimbatore, Ludhiana, Rajkot and Surat.", "locations.html",
  {"@context":"https://schema.org","@type":"CollectionPage","name":"Locations","url":SITE+"/locations.html"},
  '<div class="wrap page"><h1>Cities we support</h1><p class="lede">Our office is in Sector 3, Noida. We work with manufacturers and importers across India through video calls and online filing.</p><ul style="columns:2;margin-top:32px;padding-left:20px;line-height:2">%s</ul></div>' % items)
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
for name, content in files.items(): open(name, "w", encoding="utf-8").write(content)
print(len(files), "pages written")
