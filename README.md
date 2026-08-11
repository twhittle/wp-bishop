# Bishop &amp; Adkins, P.A. — static redesign

A 15-page static build of bishopandadkins.com, structured so every section maps
onto a native Elementor widget for rebuild in Jupiter X on WordPress.

Open `index.html` in any browser. No build step or server required.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home |
| `about.html` | About the firm |
| `services.html` | Services index |
| `tax-preparation.html` | Tax Preparation |
| `tax-planning.html` | Tax Planning, Research & Strategy |
| `estates-and-trusts.html` | Estates & Trusts |
| `quickbooks-and-bookkeeping.html` | QuickBooks Support & Bookkeeping |
| `nonprofits.html` | Nonprofits |
| `consulting.html` | Consulting |
| `staff.html` | Our Team |
| `contact.html` | Contact |
| `directions.html` | Directions |
| `client-portal.html` | Client Portal |
| `make-a-payment.html` | Make a Payment |
| `404.html` | Not found |

Plus `sitemap.xml` and `robots.txt`.

## Brand

Sampled directly from the supplied logo files.

| Token | Value | Use |
| --- | --- | --- |
| Navy | `#2D335B` | Headings, footer, primary text |
| Periwinkle | `#7285B5` | Buttons, rules, eyebrow labels |
| Bright blue | `#5B8EC4` | Accent on dark backgrounds |
| Ink | `#1B1E2B` | Footer background, hero overlay |

Type: **Playfair Display** (600/700) for headings, **Open Sans** (400/600/700)
for body — both loaded from Google Fonts and both available natively in
Jupiter X.

## Elementor mapping

No CSS grid and no JavaScript-driven layout. Each class corresponds to a widget:

| Class | Elementor widget |
| --- | --- |
| `.section` / `.container` / `.row` / `.col-*` | Flex Container |
| `.eyebrow` / `h1`–`h3` | Heading |
| `.lead` / `p` | Text Editor |
| `.btn` | Button |
| `.icon-box` | Icon Box |
| `.card` | Image Box |
| `.quote` + `.stars` | Testimonial + Star Rating |
| `.accordion` | Accordion |
| `.facts` / `.check` | Icon List |

JavaScript is limited to the mobile menu and accordion toggles — both replaced
by Jupiter X's own nav and Elementor's Accordion widget on rebuild.

## Images

All optimized: resized to a maximum of 1800px wide and converted to JPEG.
PNG is retained only where transparency is required (logos, favicon). The full
image set is about 1&nbsp;MB.

Originals are preserved untouched in `source-images/`.

## Regenerating

`build.py` generates every page from one template and one content table, so the
header, nav and footer cannot drift between pages.

```
python3 build.py
```

Site constants (phone, address, portal URLs) live at the top of that file.

## Open items

- `PORTAL_URL` and `PAYMENT_URL` in `build.py` are still `#` — set them to the
  real destinations and re-run the build.
- The contact form is markup only; it needs wiring to a form handler (Elementor
  Forms on rebuild).
- Bios for Cathy Davis, Lorie Zimmer, Stephanie Powers and Gina Blair are
  role-level placeholders. Real bios were not available; swap them in `STAFF`
  in `build.py`.
- Testimonials on the home page are representative placeholders, not real
  client quotes. Replace before publishing.
