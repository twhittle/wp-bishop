#!/usr/bin/env python3
"""Generates the Bishop & Adkins static site.

One template, one content table, so the header/nav/footer are byte-identical on
every page and no link can drift. Run:  python3 build.py
"""
import os, html

SITE = "https://www.bishopandadkins.com"
PHONE, PHONE_HREF = "(410) 893-7453", "+14108937453"
FAX, FAX_LOCAL = "(410) 838-4100", "(410) 838-2859"
STREET, CITY, STATE, ZIP = "612 Rock Spring Road", "Bel Air", "MD", "21014"
YEAR = 2026

# Fill these in when the real destinations are known.
PORTAL_URL = "#"
PAYMENT_URL = "https://buy.stripe.com/bJecN7da21hf6yP9Eh8Ra01"

SERVICES = [
    ("tax-preparation", "Tax Preparation",
     "Tax compliance for individuals, businesses, trusts, estates and nonprofits.",
     "doc"),
    ("tax-planning", "Tax Planning, Research &amp; Strategy",
     "Forward-looking strategy to reduce current and future tax liability.",
     "chart"),
    ("estates-and-trusts", "Estates &amp; Trusts",
     "Guidance for personal representatives and trustees, start to finish.",
     "shield"),
    ("quickbooks-and-bookkeeping", "QuickBooks Support &amp; Bookkeeping",
     "Set up, clean up and day-to-day support from advisors with 25+ years on the platform.",
     "book"),
    ("nonprofits", "Nonprofits",
     "Compliance and advisory work for organizations serving the community.",
     "heart"),
    ("consulting", "Consulting",
     "A sounding board for the decisions that shape your business.",
     "compass"),
]

ICONS = {
 "doc":'<path d="M6 2h9l5 5v15a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1z"/><path d="M14 2v6h6"/><path d="M9 13h7M9 17h7"/>',
 "chart":'<path d="M3 21h18"/><path d="M6 21V10M11 21V4M16 21v-8M21 21v-5"/>',
 "shield":'<path d="M12 2l8 3v7c0 5-3.4 8.7-8 10-4.6-1.3-8-5-8-10V5l8-3z"/><path d="M9 12l2 2 4-4"/>',
 "book":'<path d="M4 4a2 2 0 0 1 2-2h13v18H6a2 2 0 0 0-2 2V4z"/><path d="M8 7h7M8 11h7"/>',
 "heart":'<path d="M12 20s-7-4.4-7-9.3A4.2 4.2 0 0 1 12 7a4.2 4.2 0 0 1 7 3.7C19 15.6 12 20 12 20z"/>',
 "compass":'<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
 "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "pin":'<path d="M12 22s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="11" r="2.6"/>',
 "phone":'<path d="M21 16.9v2.6a1.7 1.7 0 0 1-1.9 1.7 17 17 0 0 1-7.4-2.6 16.6 16.6 0 0 1-5.1-5.1A17 17 0 0 1 4 6a1.7 1.7 0 0 1 1.7-1.9h2.6a1.7 1.7 0 0 1 1.7 1.5c.1 1 .3 2 .6 2.9a1.7 1.7 0 0 1-.4 1.8l-1.1 1.1a13.6 13.6 0 0 0 5.1 5.1l1.1-1.1a1.7 1.7 0 0 1 1.8-.4c.9.3 1.9.5 2.9.6a1.7 1.7 0 0 1 1.5 1.7z"/>',
 "users":'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.1a4 4 0 0 1 0 7.8"/>',
 "lock":'<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
 "card":'<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
 "award":'<circle cx="12" cy="9" r="6"/><path d="M8.5 14L7 22l5-3 5 3-1.5-8"/>',
}

def clamp(text, limit=158):
    """Trim a meta description to a word boundary under the search-snippet limit."""
    t = " ".join(text.split())
    if len(t) <= limit:
        return t
    cut = t[:limit].rsplit(" ", 1)[0].rstrip(" ,.;:—-")
    return cut + "."

# Short forms used in <title> so tags stay under ~65 characters.
SHORT = {
    "tax-preparation": "Tax Preparation",
    "tax-planning": "Tax Planning",
    "estates-and-trusts": "Estates &amp; Trusts",
    "quickbooks-and-bookkeeping": "QuickBooks &amp; Bookkeeping",
    "nonprofits": "Nonprofit Accounting",
    "consulting": "Business Consulting",
}

def icon(name, cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" focusable="false">{ICONS[name]}</svg>')

STAR = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.9-6.2-3.3-6.2 3.3L7 14.2l-5-4.9 6.9-1L12 2z"/></svg>')

def stars(n=5):
    return f'<div class="stars" role="img" aria-label="{n} out of 5 stars">' + STAR*n + '</div>'

STAFF = [
    ("rick-bishop", "Rick Bishop, CPA", "Founding Partner",
     "Rick founded Bishop &amp; Adkins in 1991. He specializes in tax planning and "
     "preparation, business consulting, business sales and acquisitions, cash flow "
     "management, business start-ups and financial statements, and works extensively "
     "with estates and trusts."),
    ("rob-adkins", "Rob Adkins, CPA/PFS, CFP&reg;", "Partner",
     "Rob joined the firm in 1995 and became a partner in 1998. Alongside his CPA "
     "license he holds the Personal Financial Specialist and CERTIFIED FINANCIAL "
     "PLANNER&trade; credentials, bringing a planning perspective to the tax work."),
    ("donna-singer", "Donna Singer, CPA/PFS", "Partner",
     "Donna joined Bishop &amp; Adkins in 2008 and became a partner the same year. She "
     "brings more than 30 years of public accounting experience along with four years "
     "in the tax department headquarters of a Fortune 500 company. Donna has been a "
     "CPA since 1983 and a Personal Financial Specialist since 2000."),
    ("cathy-davis", "Cathy Davis, CPA", "Certified Public Accountant",
     "Cathy works with individual and business clients across the firm's tax and "
     "accounting practice."),
    ("cathy-vincent", "Cathy Vincent, EA", "Enrolled Agent",
     "Cathy joined the firm in 2004. She specializes in accounting, payroll, tax "
     "return preparation and financial statements."),
    ("lorie-zimmer", "Lorie Zimmer, CPA/PFS", "Certified Public Accountant",
     "Lorie is a CPA and Personal Financial Specialist working with the firm's "
     "individual and business clients."),
    ("stephanie-powers", "Stephanie Powers", "Client Services",
     "Stephanie supports clients through the firm's tax and accounting engagements."),
    ("gina-blair", "Gina Blair", "Office Manager",
     "Gina manages the day-to-day operations of the office and is often the first "
     "person clients speak with."),
]

def nav_html(active):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    cur_attr = ' aria-current="page"'
    subs = "".join(
        '<a href="%s.html"%s>%s</a>' % (s, cur_attr if s == active else "", t)
        for s, t, _, _ in SERVICES)
    svc_cur = ' aria-current="page"' if active == "services" else ""
    return f"""<nav class="nav" id="site-nav" aria-label="Main">
        {a("index.html","Home","home")}
        {a("about.html","About","about")}
        <span class="has-sub">
          <a href="services.html"{svc_cur} aria-expanded="false">Services <span class="caret">&#9660;</span></a>
          <span class="sub">{subs}</span>
        </span>
        {a("staff.html","Our Team","staff")}
        {a("contact.html","Contact","contact")}
        {a("directions.html","Directions","directions")}
        <a class="btn btn--sm" href="client-portal.html">Client Portal</a>
      </nav>"""

def head(title, desc, canonical, schema=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{clamp(desc)}">
<link rel="canonical" href="{SITE}/{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bishop &amp; Adkins, P.A.">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{clamp(desc)}">
<meta property="og:url" content="{SITE}/{canonical}">
<meta property="og:image" content="{SITE}/assets/img/general/page-header.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="assets/img/logo/ba-favicon.png">
<link rel="apple-touch-icon" href="assets/img/logo/ba-favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{schema}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

def header(active):
    return f"""<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Bishop &amp; Adkins, P.A. — home">
      <img src="assets/img/logo/ba-logo.png" alt="Bishop &amp; Adkins, P.A., Certified Public Accountants" width="808" height="211">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
    {nav_html(active)}
  </div>
</header>
<div class="nav-backdrop" aria-hidden="true"></div>
<main id="main">
"""

CTA = f"""<section class="cta">
  <div class="container">
    <h2>Let&rsquo;s talk about your situation</h2>
    <p>Whether it&rsquo;s a return, a business decision or an estate you didn&rsquo;t expect to be managing, a short conversation is usually the fastest way forward.</p>
    <a class="cta-phone" href="tel:{PHONE_HREF}">{PHONE}</a>
    <div class="btn-group">
      <a class="btn" href="contact.html">Contact the Office</a>
      <a class="btn btn--light" href="directions.html">Get Directions</a>
    </div>
  </div>
</section>"""

def footer():
    svc = "".join(f'<li><a href="{s}.html">{t}</a></li>' for s, t, _, _ in SERVICES)
    return f"""</main>
<footer class="site-footer">
  <div class="container">
    <div class="row">
      <div class="footer-brand">
        <img class="footer-logo" src="assets/img/logo/ba-logo-inverted.png" alt="Bishop &amp; Adkins, P.A." width="770" height="196">
        <p>A full-service tax and accounting firm serving Bel Air and Harford County since 1991. Registered with the Maryland State Board of Public Accountants.</p>
      </div>
      <div class="footer-col">
        <h2>Services</h2>
        <ul class="footer-links">{svc}</ul>
      </div>
      <div class="footer-col">
        <h2>Firm</h2>
        <ul class="footer-links">
          <li><a href="about.html">About</a></li>
          <li><a href="staff.html">Our Team</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="directions.html">Directions</a></li>
          <li><a href="client-portal.html">Client Portal</a></li>
          <li><a href="make-a-payment.html">Make a Payment</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h2>Office</h2>
        <address>
          {STREET}<br>{CITY}, {STATE} {ZIP}<br><br>
          <a href="tel:{PHONE_HREF}">{PHONE}</a><br>
          Fax {FAX}<br>
          Local fax {FAX_LOCAL}
        </address>
        <p style="margin-top:16px">Mon&ndash;Fri 8:00am&ndash;5:00pm<br>Sat 9:00am&ndash;5:00pm<br>Sun closed</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; {YEAR} Bishop &amp; Adkins, P.A. All rights reserved.</span>
      <span>Certified Public Accountants &middot; {CITY}, Maryland</span>
    </div>
  </div>
</footer>
<script src="assets/js/site.js"></script>
</body>
</html>
"""

SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "AccountingService",
  "name": "Bishop & Adkins, P.A.",
  "description": "Full-service certified public accounting firm providing tax preparation, tax planning, estates and trusts, bookkeeping, payroll and consulting in Bel Air, Maryland.",
  "url": "https://www.bishopandadkins.com",
  "telephone": "+1-410-893-7453",
  "faxNumber": "+1-410-838-4100",
  "foundingDate": "1991",
  "image": "https://www.bishopandadkins.com/assets/img/general/rebecca-house.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "612 Rock Spring Road",
    "addressLocality": "Bel Air",
    "addressRegion": "MD",
    "postalCode": "21014",
    "addressCountry": "US"
  },
  "areaServed": ["Bel Air", "Harford County", "Maryland"],
  "openingHoursSpecification": [
    {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"17:00"},
    {"@type":"OpeningHoursSpecification","dayOfWeek":["Saturday"],"opens":"09:00","closes":"17:00"}
  ]
}
</script>"""

def page_hero(title, sub, crumb=None, img="assets/img/general/page-header.jpg"):
    bc = ""
    if crumb:
        bc = ('<p class="breadcrumb"><a href="index.html">Home</a> &nbsp;&rsaquo;&nbsp; '
              + crumb + "</p>")
    return f"""<section class="hero page-hero" style="background-image:url('{img}')">
  <div class="container">
    <div class="hero-copy">
      {bc}
      <h1>{title}</h1>
      <hr class="rule rule--light">
      <p>{sub}</p>
    </div>
  </div>
</section>"""

def write(name, body):
    with open(name, "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote", name)


# ---------------------------------------------------------------- HOME ------
def build_home():
    boxes = ""
    for slug, title, blurb, ic in SERVICES:
        boxes += f"""<div class="col-3">
          <div class="icon-box">
            <span class="ico">{icon(ic)}</span>
            <h3>{title}</h3>
            <p>{blurb}</p>
            <a class="more" href="{slug}.html">Read more &rarr;</a>
          </div>
        </div>"""
    partners = ""
    for slug, name, role, _ in STAFF[:3]:
        partners += f"""<div class="col-3">
          <div class="card">
            <img src="assets/img/staff/{slug}.jpg" alt="{html.escape(name.replace('&amp;','&').replace('&reg;','')).strip()}, {role} at Bishop &amp; Adkins, P.A." width="350" height="450" loading="lazy">
            <div class="card-body">
              <h3>{name}</h3>
              <p class="card-role">{role}</p>
            </div>
          </div>
        </div>"""

    quotes = [
      ("They have handled our family&rsquo;s returns and my business books for years. Questions get answered the same day, and nothing falls through the cracks.", "Business owner, Bel Air"),
      ("When my father passed, I had no idea what was involved in settling the estate. They walked me through every filing and deadline.", "Estate client, Harford County"),
      ("Straightforward advice, no jargon, and they actually tell you when something isn&rsquo;t worth doing.", "Individual tax client"),
    ]
    qhtml = "".join(f"""<div class="col-3"><div class="quote">{stars()}<p>&ldquo;{q}&rdquo;</p><cite>&mdash; {c}</cite></div></div>""" for q, c in quotes)

    body = head(
        "Bishop &amp; Adkins, P.A. | Certified Public Accountants in Bel Air, MD",
        "Bishop &amp; Adkins, P.A. is a full-service CPA firm in Bel Air, Maryland offering tax preparation, tax planning, estates and trusts, QuickBooks and bookkeeping, nonprofit and consulting services since 1991.",
        "", SCHEMA) + header("home") + f"""
<section class="hero" style="background-image:url('assets/img/general/home-hero.jpg')">
  <div class="container">
    <div class="hero-copy">
      <p class="eyebrow">Certified Public Accountants &middot; Since 1991</p>
      <h1>Thoughtful tax and accounting for Harford County</h1>
      <hr class="rule rule--light">
      <p>A full-service firm in the heart of Bel Air, working with individuals, businesses, estates and nonprofits &mdash; the same people, year after year.</p>
      <div class="btn-group">
        <a class="btn" href="services.html">Explore Our Services</a>
        <a class="btn btn--light" href="contact.html">Talk to Us</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="row row--middle row--split">
      <div class="col-2">
        <p class="eyebrow">Who we are</p>
        <h2>A firm small enough to know you, large enough to handle it</h2>
        <hr class="rule">
        <p class="lead">Bishop &amp; Adkins, P.A. is a quality full-service tax and accounting firm registered with the Maryland State Board of Public Accountants. For more than three decades we have helped clients across Bel Air and Harford County meet their obligations and plan for what comes next.</p>
        <p>Our team&rsquo;s experience runs from straightforward individual returns to complex multi-state filings, rental and vacation property, stock options and grants, and complicated investment accounts. Whatever arrives in your mailbox from the IRS, we have almost certainly seen it before.</p>
        <div class="btn-group" style="margin-top:26px">
          <a class="btn btn--outline" href="about.html">More About the Firm</a>
        </div>
      </div>
      <div class="col-2 media">
        <img src="assets/img/general/firm.jpg" alt="The Bishop &amp; Adkins, P.A. team in Bel Air, Maryland" width="1000" height="600" loading="lazy">
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head text-center">
      <p class="eyebrow">What we do</p>
      <h2>Services</h2>
      <hr class="rule rule--center">
      <p class="lead">Tax compliance and planning, accounting support and the advice that surrounds both.</p>
    </div>
    <div class="row">{boxes}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="row row--middle row--split">
      <div class="col-2 media">
        <img src="assets/img/general/rebecca-house.jpg" alt="The Rebecca House, an 1886 Victorian home at 612 Rock Spring Road that houses Bishop &amp; Adkins" width="1000" height="500" loading="lazy">
        <p class="figure-caption">The Rebecca House, built 1886 &mdash; our offices in Bel Air&rsquo;s historic district.</p>
      </div>
      <div class="col-2">
        <p class="eyebrow">Since 1991</p>
        <h2>An 1886 Victorian in Bel Air&rsquo;s historic district</h2>
        <hr class="rule">
        <p>Our office sits in the Town of Bel Air&rsquo;s historic district at 612 Rock Spring Road. Built in 1886 and known as the Rebecca House, the Victorian now serves as the home of Bishop &amp; Adkins, P.A.</p>
        <p>It is a fitting building for a practice built on continuity &mdash; Rick Bishop founded the firm in 1991, Rob Adkins joined in 1995, and Donna Singer came aboard in 2008. Many of our clients have worked with the same accountant here for twenty years or more.</p>
        <ul class="facts">
          <li><span class="lbl">Founded</span><span>1991 by Rick Bishop, CPA</span></li>
          <li><span class="lbl">Registered</span><span>Maryland State Board of Public Accountants</span></li>
          <li><span class="lbl">Serving</span><span>Bel Air &amp; Harford County, Maryland</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head text-center">
      <p class="eyebrow">Our people</p>
      <h2>The partners</h2>
      <hr class="rule rule--center">
    </div>
    <div class="row">{partners}</div>
    <div class="btn-group" style="justify-content:center;margin-top:44px">
      <a class="btn btn--outline" href="staff.html">Meet the Full Team</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head text-center">
      <p class="eyebrow">In their words</p>
      <h2>What clients tell us</h2>
      <hr class="rule rule--center">
    </div>
    <div class="row">{qhtml}</div>
  </div>
</section>

{CTA}
""" + footer()
    write("index.html", body)


# --------------------------------------------------------------- ABOUT ------
def build_about():
    timeline = [
        ("1991", "Rick Bishop, CPA founds the firm", "Bishop &amp; Adkins opens its doors in Bel Air, built around tax planning and preparation, business consulting and work with estates and trusts."),
        ("1995", "Rob Adkins, CPA joins", "Rob joins the practice, going on to become a partner three years later."),
        ("1998", "Rob Adkins becomes partner", "The firm takes the name it carries today."),
        ("2008", "Donna Singer, CPA/PFS joins and becomes partner", "Donna arrives with more than three decades of public accounting experience and Fortune 500 corporate tax background."),
        ("Today", "Three partners, one office, the same block", "A full-service firm serving individuals, businesses of every type, trusts, estates and nonprofits across Harford County."),
    ]
    tl = ""
    for yr, ttl, txt in timeline:
        tl += f"""<div class="col-2">
          <div class="panel panel--accent">
            <p class="eyebrow">{yr}</p>
            <h3>{ttl}</h3>
            <p>{txt}</p>
          </div>
        </div>"""
    values = [
        ("users", "Continuity", "You are not reassigned each season. The person who prepared your return last year is very likely preparing it again."),
        ("award", "Credentials that matter", "CPAs, Enrolled Agents, Personal Financial Specialists and a CERTIFIED FINANCIAL PLANNER&trade; professional under one roof."),
        ("clock", "Answers when you need them", "Deadlines do not move. We keep you ahead of them rather than reacting to them."),
    ]
    vh = "".join(f"""<div class="col-3"><div class="icon-box"><span class="ico">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></div></div>""" for ic, t, d in values)

    body = head(
        "About Our Firm | Bishop &amp; Adkins, P.A. | Bel Air, MD CPAs",
        "Founded in 1991 by Rick Bishop, CPA, Bishop &amp; Adkins is a full-service CPA firm in Bel Air, Maryland, housed in the historic 1886 Rebecca House and registered with the Maryland State Board of Public Accountants.",
        "about.html") + header("about") + page_hero(
        "About the Firm",
        "Three decades of tax and accounting work from one Victorian house on Rock Spring Road.",
        "About") + f"""
<section class="section">
  <div class="container container--narrow">
    <p class="eyebrow">Our story</p>
    <h2>A quality full-service tax and accounting firm</h2>
    <hr class="rule">
    <p class="lead">Bishop &amp; Adkins, P.A. is a registered certified public accounting firm with the Maryland State Board of Public Accountants, serving Bel Air and the surrounding Harford County communities for more than thirty years.</p>
    <p>We provide tax compliance services for individuals &mdash; including gift tax returns &mdash; businesses of all types, trusts, estates and nonprofits. Around that core sits everything the work tends to require: tax planning and research, QuickBooks support and bookkeeping, financial statements, payroll and consulting.</p>
    <p>Our team members&rsquo; experience ranges from basic returns to complex multi-state filings, and we are well equipped to handle rental and vacation properties, stock options and grants, and complicated investment accounts.</p>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head text-center">
      <p class="eyebrow">How we got here</p>
      <h2>A short history</h2>
      <hr class="rule rule--center">
    </div>
    <div class="row">{tl}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="row row--middle row--split">
      <div class="col-2 media">
        <img src="assets/img/general/rebecca-house.jpg" alt="Exterior of the Rebecca House, the 1886 Victorian home at 612 Rock Spring Road, Bel Air" width="1000" height="500" loading="lazy">
      </div>
      <div class="col-2">
        <p class="eyebrow">The Rebecca House</p>
        <h2>Built in 1886, working since</h2>
        <hr class="rule">
        <p>The Bishop &amp; Adkins office is located in the Town of Bel Air&rsquo;s historic district at 612 Rock Spring Road. The Victorian house on the property was built in 1886 and is known as the Rebecca House. It now serves as the office building for the firm.</p>
        <p>One practical note for first-time visitors: the entrance is not on Rock Spring Road. Come in from E Howard Street and follow the alley about 200 feet to the second house on the right.</p>
        <div class="btn-group" style="margin-top:24px">
          <a class="btn btn--outline" href="directions.html">Full Directions</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head text-center">
      <p class="eyebrow">What you can expect</p>
      <h2>How we work</h2>
      <hr class="rule rule--center">
    </div>
    <div class="row">{vh}</div>
  </div>
</section>

{CTA}
""" + footer()
    write("about.html", body)


# ------------------------------------------------------------ SERVICES ------
SERVICE_CONTENT = {
 "tax-preparation": {
   "sub": "Compliance work for individuals, businesses, trusts, estates and nonprofits.",
   "lead": "B&amp;A offers tax compliance services for individuals &mdash; including gift tax returns &mdash; businesses of all types, trusts, estates and nonprofits.",
   "body": ["Our team members have extensive experience ranging from basic returns to complex multi-state returns, and are well equipped to handle a wide range of tax issues.",
            "Returns are prepared and reviewed in-house by the same people year after year, which means the history of your situation stays with the file rather than having to be re-explained each season."],
   "list_title": "Situations we handle regularly",
   "list": ["Individual returns, including gift tax returns",
            "Businesses of all types &mdash; sole proprietors through corporations",
            "Trust, estate and nonprofit returns",
            "Complex multi-state filings",
            "Rental and vacation properties",
            "Stock options and grants",
            "Complicated investment accounts"],
 },
 "tax-planning": {
   "sub": "Looking forward rather than backward, so April holds fewer surprises.",
   "lead": "We help you plan for &mdash; and potentially minimize &mdash; your current and future tax liabilities.",
   "body": ["Tax law does not sit still. We stay up to date with changes and developments so that we can recommend strategies that may save you money, and so that decisions you are weighing now are made with their tax consequences understood.",
            "Planning conversations tend to be most valuable before a transaction rather than after it. If you are considering a sale, a purchase, a change in entity structure or a significant shift in income, that is the moment to call."],
   "list_title": "Where planning pays off",
   "list": ["Anticipating liability before the year closes",
            "Timing of income and deductions",
            "Entity structure and accounting method choices",
            "Retirement and investment decisions with tax consequences",
            "Research on new or changing tax law as it applies to you"],
 },
 "estates-and-trusts": {
   "sub": "Steady guidance for personal representatives and trustees.",
   "lead": "Many clients find themselves in the position of managing the estate of a deceased family member, or administering a trust.",
   "body": ["It is rarely a role anyone volunteers for, and it usually arrives at a difficult time. We work directly with the personal representative or trustee to facilitate the preparation of estate and trust tax returns and to make the requirements clear.",
            "Our aim is that you understand what has to be filed, by when, and what your responsibilities are &mdash; so the administrative side takes as little of your attention as possible."],
   "list_title": "How we help",
   "list": ["Preparation of estate and trust tax returns",
            "Working alongside the personal representative or trustee",
            "Clarifying filing requirements and deadlines",
            "Coordinating with attorneys and other advisors",
            "Ongoing trust compliance year to year"],
 },
 "quickbooks-and-bookkeeping": {
   "sub": "A general ledger you can actually run a business from.",
   "lead": "Maintaining a general ledger is an integral part of a successful business accounting system.",
   "body": ["B&amp;A can help you create and manage the system that is right for you and your business, organizing your financial records so they guide you in managing the business and satisfy IRS requirements at the same time.",
            "As QuickBooks advisors with over 25 years of experience, our team can advise on proper set-up and efficient use of accounting systems, and assist with day-to-day usage, reconciliations and reporting."],
   "list_title": "What this looks like in practice",
   "list": ["QuickBooks set-up, clean-up and file review",
            "Day-to-day usage support and troubleshooting",
            "Account reconciliations",
            "Financial statement preparation",
            "Payroll",
            "Reporting you can actually use to make decisions"],
 },
 "nonprofits": {
   "sub": "Compliance and advice for organizations serving the community.",
   "lead": "B&amp;A understands the challenges that nonprofit organizations face.",
   "body": ["Our experience enables us to provide guidance, advice and the fulfillment of compliance obligations &mdash; without losing sight of the fact that every hour spent on administration is an hour not spent on the mission.",
            "We work with boards, executive directors and treasurers to keep filings current and reporting clear enough to hand to a funder or a board meeting without translation."],
   "list_title": "Support for nonprofit organizations",
   "list": ["Annual information return preparation",
            "Compliance obligations and deadlines",
            "Financial statements for boards and funders",
            "Bookkeeping and accounting system support",
            "General guidance and advice for board and staff"],
 },
 "consulting": {
   "sub": "A sounding board for decisions with financial consequences.",
   "lead": "Our staff can guide you through personal tax decisions and business decisions alike.",
   "body": ["Some questions do not fit neatly into a filing season. Whether you are buying or selling a business, deciding whether to lease or buy equipment, or settling on an accounting method, the choice usually carries tax and cash flow consequences worth thinking through in advance.",
            "Because we already know your history, these conversations tend to start further along than they would with someone seeing your numbers for the first time."],
   "list_title": "Decisions we are often asked about",
   "list": ["Business purchases and sales",
            "Leasing versus buying equipment",
            "Determining accounting methods",
            "Business start-ups and entity selection",
            "Cash flow management",
            "Personal tax decisions with long horizons"],
 },
}

def build_services_index():
    boxes = ""
    for slug, title, blurb, ic in SERVICES:
        boxes += f"""<div class="col-3">
          <div class="icon-box">
            <span class="ico">{icon(ic)}</span>
            <h3>{title}</h3>
            <p>{blurb}</p>
            <a class="more" href="{slug}.html">Read more &rarr;</a>
          </div>
        </div>"""
    body = head(
        "Services | Bishop &amp; Adkins, P.A. | CPAs in Bel Air, Maryland",
        "Tax preparation, tax planning, estates and trusts, QuickBooks and bookkeeping, nonprofit services and business consulting from Bishop &amp; Adkins, P.A. in Bel Air, MD.",
        "services.html") + header("services") + page_hero(
        "Services",
        "Tax compliance and planning, accounting support, and the advice that surrounds both.",
        "Services") + f"""
<section class="section">
  <div class="container">
    <div class="section-head text-center">
      <p class="eyebrow">Full service</p>
      <h2>Everything a tax and accounting practice should cover</h2>
      <hr class="rule rule--center">
      <p class="lead">We provide tax compliance for individuals, businesses of all types, trusts, estates and nonprofits &mdash; together with planning, bookkeeping, financial statements, payroll and consulting.</p>
    </div>
    <div class="row">{boxes}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--narrow text-center">
    <h2>Not sure which of these you need?</h2>
    <hr class="rule rule--center">
    <p class="lead">Most clients arrive with a situation rather than a service in mind. Describe it to us and we will tell you what is actually involved.</p>
    <div class="btn-group" style="justify-content:center;margin-top:26px">
      <a class="btn" href="contact.html">Start a Conversation</a>
    </div>
  </div>
</section>

{CTA}
""" + footer()
    write("services.html", body)


def build_service_pages():
    for slug, title, blurb, ic in SERVICES:
        c = SERVICE_CONTENT[slug]
        others = "".join(
            f"""<div class="col-3"><div class="icon-box"><span class="ico">{icon(i2)}</span><h3>{t2}</h3><p>{b2}</p><a class="more" href="{s2}.html">Read more &rarr;</a></div></div>"""
            for s2, t2, b2, i2 in SERVICES if s2 != slug)
        bullets = "".join(f"<li>{x}</li>" for x in c["list"])
        paras = "".join(f"<p>{p}</p>" for p in c["body"])
        plain = title.replace("&amp;", "and")
        lead_plain = (c["lead"].replace("&amp;", "and").replace("&mdash;", "—")
                      .replace("&rsquo;", "'"))
        body = head(
            f"{SHORT[slug]} | Bishop &amp; Adkins, P.A. | Bel Air, MD",
            clamp(f"{lead_plain} Bishop &amp; Adkins, P.A., CPAs in Bel Air, Maryland."),
            f"{slug}.html") + header("services") + page_hero(
            title, c["sub"],
            f'<a href="services.html">Services</a> &nbsp;&rsaquo;&nbsp; {title}') + f"""
<section class="section">
  <div class="container">
    <div class="row row--split">
      <div class="col-2">
        <p class="eyebrow">Overview</p>
        <h2>{title}</h2>
        <hr class="rule">
        <p class="lead">{c['lead']}</p>
        {paras}
      </div>
      <div class="col-2">
        <div class="panel panel--accent">
          <h3>{c['list_title']}</h3>
          <ul class="check">{bullets}</ul>
          <a class="btn" href="contact.html">Ask About {plain.split(',')[0]}</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head text-center">
      <p class="eyebrow">Also from B&amp;A</p>
      <h2>Other services</h2>
      <hr class="rule rule--center">
    </div>
    <div class="row">{others}</div>
  </div>
</section>

{CTA}
""" + footer()
        write(f"{slug}.html", body)


# ---------------------------------------------------------------- TEAM ------
def build_staff():
    def card(idx, s):
        slug, name, role, bio = s
        clean = name.replace("&amp;", "and").replace("&reg;", "").replace("&trade;", "")
        return f"""<div class="col-3">
          <div class="card">
            <img src="assets/img/staff/{slug}.jpg" alt="Portrait of {clean}, {role} at Bishop &amp; Adkins, P.A." width="350" height="450" loading="lazy">
            <div class="card-body">
              <h3>{name}</h3>
              <p class="card-role">{role}</p>
              <p>{bio}</p>
            </div>
          </div>
        </div>"""
    partners = "".join(card(i, s) for i, s in enumerate(STAFF[:3]))
    team = "".join(card(i, s) for i, s in enumerate(STAFF[3:]))

    body = head(
        "Our Team | Bishop &amp; Adkins, P.A. | Bel Air, MD CPAs",
        "Meet the CPAs, Enrolled Agents and staff of Bishop &amp; Adkins, P.A. in Bel Air, Maryland — partners Rick Bishop, Rob Adkins and Donna Singer and the team behind them.",
        "staff.html") + header("staff") + page_hero(
        "Our Team",
        "The people who will actually be working on your return &mdash; the same ones next year.",
        "Our Team") + f"""
<section class="section">
  <div class="container">
    <div class="section-head text-center">
      <p class="eyebrow">Leadership</p>
      <h2>The partners</h2>
      <hr class="rule rule--center">
    </div>
    <div class="row">{partners}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head text-center">
      <p class="eyebrow">Our staff</p>
      <h2>The team</h2>
      <hr class="rule rule--center">
    </div>
    <div class="row">{team}</div>
  </div>
</section>

{CTA}
""" + footer()
    write("staff.html", body)


# ------------------------------------------------------------- CONTACT ------
def build_contact():
    opts = "".join(f'<option value="{t.replace("&amp;","and")}">{t}</option>' for _, t, _, _ in SERVICES)
    body = head(
        "Contact | Bishop &amp; Adkins, P.A. | (410) 893-7453 | Bel Air, MD",
        "Contact Bishop &amp; Adkins, P.A. at 612 Rock Spring Road, Bel Air, MD 21014. Call (410) 893-7453. Open Monday to Friday 8am–5pm and Saturday 9am–5pm.",
        "contact.html", SCHEMA) + header("contact") + page_hero(
        "Contact Us",
        "Call the office, send a note, or stop by &mdash; we are on Rock Spring Road in Bel Air.",
        "Contact") + f"""
<section class="section">
  <div class="container">
    <div class="row row--split">
      <div class="col-2">
        <p class="eyebrow">Get in touch</p>
        <h2>Send us a message</h2>
        <hr class="rule">
        <p>Tell us a little about your situation and the right person here will get back to you. If it is time-sensitive, calling is always faster.</p>
        <form id="contact-form" novalidate>
          <div class="form-row">
            <div class="field">
              <label for="name">Name</label>
              <input type="text" id="name" name="name" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="phone">Phone</label>
              <input type="tel" id="phone" name="phone" autocomplete="tel">
            </div>
          </div>
          <div class="form-row">
            <div class="field field--full">
              <label for="email">Email</label>
              <input type="email" id="email" name="email" autocomplete="email" required>
            </div>
          </div>
          <div class="form-row">
            <div class="field field--full">
              <label for="topic">What can we help with?</label>
              <select id="topic" name="topic">
                <option value="">Please choose&hellip;</option>
                {opts}
                <option value="Something else">Something else</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="field field--full">
              <label for="message">Message</label>
              <textarea id="message" name="message" required></textarea>
            </div>
          </div>
          <button class="btn" type="submit">Send Message</button>
          <p class="form-note" id="form-status">Please do not send sensitive documents or Social Security numbers through this form &mdash; use the secure Client Portal instead.</p>
        </form>
      </div>
      <div class="col-2">
        <div class="panel">
          <h3>Office details</h3>
          <hr class="rule">
          <ul class="facts">
            <li><span class="lbl">Address</span><span>{STREET}<br>{CITY}, {STATE} {ZIP}</span></li>
            <li><span class="lbl">Phone</span><span><a href="tel:{PHONE_HREF}">{PHONE}</a></span></li>
            <li><span class="lbl">Fax</span><span>{FAX}</span></li>
            <li><span class="lbl">Local fax</span><span>{FAX_LOCAL}</span></li>
          </ul>
          <h3 style="margin-top:34px">Office hours</h3>
          <hr class="rule">
          <ul class="facts">
            <li><span class="lbl">Mon&ndash;Fri</span><span>8:00am &ndash; 5:00pm</span></li>
            <li><span class="lbl">Saturday</span><span>9:00am &ndash; 5:00pm</span></li>
            <li><span class="lbl">Sunday</span><span>Closed</span></li>
          </ul>
          <div class="btn-group" style="margin-top:28px">
            <a class="btn btn--outline" href="directions.html">Get Directions</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section--tight section--alt">
  <div class="container">
    <div class="notice">
      <p><strong>Finding us:</strong> the entrance is not on Rock Spring Road. Turn off E Howard Street and follow the alley roughly 200 feet to the second house on the right. <a href="directions.html">Full directions &rarr;</a></p>
    </div>
  </div>
</section>

<a href="https://www.google.com/maps/search/?api=1&amp;query=612+Rock+Spring+Road+Bel+Air+MD+21014" target="_blank" rel="noopener" aria-label="Open 612 Rock Spring Road in Google Maps">
  <img src="assets/img/general/map.jpg" alt="Map showing Bishop &amp; Adkins in Bel Air, Maryland, north-east of Baltimore" width="1400" height="650" loading="lazy" style="width:100%">
</a>

{CTA}
""" + footer()
    write("contact.html", body)


# ---------------------------------------------------------- DIRECTIONS ------
def build_directions():
    body = head(
        "Directions | Bishop &amp; Adkins, P.A. | Bel Air, MD",
        "Directions to Bishop &amp; Adkins, P.A. at 612 Rock Spring Road, Bel Air, MD 21014. The entrance is off E Howard Street — follow the alley about 200 feet to the second house on the right.",
        "directions.html", SCHEMA) + header("directions") + page_hero(
        "Directions",
        "We are in Bel Air&rsquo;s historic district &mdash; with one turn that catches first-time visitors.",
        "Directions") + f"""
<section class="section">
  <div class="container">
    <div class="row row--split">
      <div class="col-2">
        <p class="eyebrow">Finding the office</p>
        <h2>The entrance is not on Rock Spring Road</h2>
        <hr class="rule">
        <div class="notice" style="margin-bottom:28px">
          <p><strong>Important:</strong> although our address is {STREET}, you cannot enter from Rock Spring Road. Turn onto <strong>E Howard Street</strong> and follow the alley approximately <strong>200 feet</strong> from Rock Spring Road. We are the <strong>second house on the right</strong>.</p>
        </div>
        <p>Look for the 1886 Victorian &mdash; the Rebecca House. It is the building itself, not a suite inside a larger complex, so once you are on the alley it is hard to miss.</p>
        <ul class="facts">
          <li><span class="lbl">Address</span><span>{STREET}<br>{CITY}, {STATE} {ZIP}</span></li>
          <li><span class="lbl">Enter from</span><span>E Howard Street, via the alley</span></li>
          <li><span class="lbl">Landmark</span><span>The Rebecca House, second on the right</span></li>
          <li><span class="lbl">Phone</span><span><a href="tel:{PHONE_HREF}">{PHONE}</a></span></li>
        </ul>
        <div class="btn-group" style="margin-top:28px">
          <a class="btn" href="https://www.google.com/maps/dir/?api=1&amp;destination=612+Rock+Spring+Road+Bel+Air+MD+21014" target="_blank" rel="noopener">Open in Google Maps</a>
          <a class="btn btn--outline" href="tel:{PHONE_HREF}">Call for Help</a>
        </div>
      </div>
      <div class="col-2 media">
        <img src="assets/img/general/rebecca-house.jpg" alt="The Rebecca House at 612 Rock Spring Road, Bel Air, Maryland" width="1000" height="500" loading="lazy">
        <p class="figure-caption">Look for this building &mdash; the Rebecca House, built 1886.</p>
      </div>
    </div>
  </div>
</section>

<section class="section--tight">
  <div class="container">
    <a href="https://www.google.com/maps/search/?api=1&amp;query=612+Rock+Spring+Road+Bel+Air+MD+21014" target="_blank" rel="noopener" aria-label="Open our location in Google Maps">
      <img src="assets/img/general/map.jpg" alt="Regional map showing Bel Air, Maryland and the location of Bishop &amp; Adkins relative to Baltimore" width="1400" height="650" loading="lazy">
    </a>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head text-center">
      <p class="eyebrow">Before you visit</p>
      <h2>Office hours</h2>
      <hr class="rule rule--center">
    </div>
    <div class="row">
      <div class="col-3"><div class="icon-box"><span class="ico">{icon('clock')}</span><h3>Monday &ndash; Friday</h3><p>8:00am &ndash; 5:00pm</p></div></div>
      <div class="col-3"><div class="icon-box"><span class="ico">{icon('clock')}</span><h3>Saturday</h3><p>9:00am &ndash; 5:00pm</p></div></div>
      <div class="col-3"><div class="icon-box"><span class="ico">{icon('pin')}</span><h3>Sunday</h3><p>Closed</p></div></div>
    </div>
  </div>
</section>

{CTA}
""" + footer()
    write("directions.html", body)


# -------------------------------------------------------------- PORTAL ------
def build_portal():
    steps = [("lock","Sign in securely","Use the credentials the office issued you. The portal is encrypted end to end, unlike email."),
             ("doc","Upload and download","Send documents to us and retrieve completed returns without a trip to Rock Spring Road."),
             ("phone","Need access?","Call the office and we will set you up or reset your credentials.")]
    sh = "".join(f"""<div class="col-3"><div class="icon-box"><span class="ico">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div></div>""" for i,t,d in steps)
    body = head(
        "Client Portal | Bishop &amp; Adkins, P.A. | Secure Document Exchange",
        "Securely exchange tax documents with Bishop &amp; Adkins, P.A. through the client portal. Call (410) 893-7453 for access.",
        "client-portal.html") + header("portal") + page_hero(
        "Client Portal",
        "A secure way to send us documents &mdash; and to collect your finished return.",
        "Client Portal") + f"""
<section class="section">
  <div class="container container--narrow text-center">
    <p class="eyebrow">Secure access</p>
    <h2>Sign in to your account</h2>
    <hr class="rule rule--center">
    <p class="lead">The client portal lets you exchange sensitive documents with our office safely. Please use it rather than email for anything containing Social Security numbers, account numbers or financial statements.</p>
    <div class="btn-group" style="justify-content:center;margin-top:30px">
      <a class="btn" href="{PORTAL_URL}">Open the Client Portal</a>
      <a class="btn btn--outline" href="tel:{PHONE_HREF}">Call for Access</a>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="row">{sh}</div>
  </div>
</section>

{CTA}
""" + footer()
    write("client-portal.html", body)


def build_payment():
    body = head(
        "Make a Payment | Bishop &amp; Adkins, P.A. | Bel Air, MD",
        "Pay your Bishop &amp; Adkins, P.A. invoice online, or by check or phone. Questions about an invoice? Call (410) 893-7453.",
        "make-a-payment.html") + header("payment") + page_hero(
        "Make a Payment",
        "Settle an invoice online, by mail or over the phone.",
        "Make a Payment") + f"""
<section class="section">
  <div class="container container--narrow text-center">
    <p class="eyebrow">Billing</p>
    <h2>Pay your invoice</h2>
    <hr class="rule rule--center">
    <p class="lead">Have your invoice number to hand. If anything on the invoice is unclear, please call the office before paying &mdash; we would rather answer the question first.</p>
    <div class="btn-group" style="justify-content:center;margin-top:30px">
      <a class="btn" href="{PAYMENT_URL}">Pay Online</a>
      <a class="btn btn--outline" href="tel:{PHONE_HREF}">Pay by Phone</a>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="row">
      <div class="col-3"><div class="icon-box"><span class="ico">{icon('card')}</span><h3>Online</h3><p>Pay by card or bank transfer using the button above. You will need your invoice number.</p></div></div>
      <div class="col-3"><div class="icon-box"><span class="ico">{icon('phone')}</span><h3>By phone</h3><p>Call <a href="tel:{PHONE_HREF}">{PHONE}</a> during office hours and we can take payment directly.</p></div></div>
      <div class="col-3"><div class="icon-box"><span class="ico">{icon('pin')}</span><h3>By mail</h3><p>{STREET}<br>{CITY}, {STATE} {ZIP}</p></div></div>
    </div>
  </div>
</section>

{CTA}
""" + footer()
    write("make-a-payment.html", body)


def build_404():
    body = head("Page Not Found | Bishop &amp; Adkins, P.A.",
                "The page you were looking for could not be found. Return to the Bishop & Adkins, P.A. home page or call (410) 893-7453.",
                "404.html") + header("") + f"""
<section class="section" style="padding:120px 0">
  <div class="container container--narrow text-center">
    <p class="eyebrow">Error 404</p>
    <h1>We couldn&rsquo;t find that page</h1>
    <hr class="rule rule--center">
    <p class="lead">The link may be out of date, or the page may have moved. Here are the places people usually want.</p>
    <div class="btn-group" style="justify-content:center;margin-top:30px">
      <a class="btn" href="index.html">Back to Home</a>
      <a class="btn btn--outline" href="services.html">Our Services</a>
    </div>
  </div>
</section>
""" + footer()
    write("404.html", body)


def build_sitemap():
    pages = ["", "about.html", "services.html"] + [f"{s}.html" for s,_,_,_ in SERVICES] + \
            ["staff.html", "contact.html", "directions.html", "client-portal.html", "make-a-payment.html"]
    urls = "".join(f"  <url><loc>{SITE}/{p}</loc></url>\n" for p in pages)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build_home(); build_about(); build_services_index(); build_service_pages()
    build_staff(); build_contact(); build_directions(); build_portal()
    build_payment(); build_404(); build_sitemap()
    print("\nDone.")
