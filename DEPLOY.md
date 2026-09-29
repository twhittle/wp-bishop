# Moving the site out of `/2026/`

The static build is written for the domain root: every internal link is
relative, there is no `<base>` tag, and all 15 `<link rel="canonical">` tags
already point at `https://www.bishopandadkins.com/…` with no `/2026/` in them.
Nothing in the HTML has to change. The only work is on the server — the files
are in the wrong folder.

Host: A2 Hosting shared cPanel (68.66.200.215). Steps below are cPanel File
Manager.

---

## Step 0 — Back up first (do not skip)

cPanel → **Files → Backup** → *Download a Home Directory Backup*. Wait for it
to finish before touching anything. If there is a WordPress site at the root,
also take a database backup from *Download a MySQL Database Backup*.

A faster in-place alternative: in File Manager, select `public_html`, click
**Compress**, and keep the resulting `.zip` outside `public_html`.

---

## Step 1 — See what is at the root

Open File Manager and look at `public_html`. You are in one of two cases.

**Case A — the root is empty or just a placeholder** (only an `index.html`,
`default.html`, a cPanel `cgi-bin`, and the `2026` folder). Go to Step 2.

**Case B — the old WordPress site is at the root** (you see `wp-admin`,
`wp-content`, `wp-includes`, `wp-config.php`, `index.php`, `.htaccess`). Do
Step 1b first.

### Step 1b — Park WordPress (Case B only)

Do not delete it. Move it aside so it stops being served but stays recoverable:

1. In `public_html`, click **+ Folder** and create `_wp-archive`.
2. Select every WordPress item — `wp-admin`, `wp-content`, `wp-includes`,
   `wp-config.php`, `index.php`, `xmlrpc.php`, `wp-*.php`, `license.txt`,
   `readme.html`, and the existing `.htaccess` — but **not** `2026`,
   `_wp-archive`, or `cgi-bin`.
3. **Move** them into `_wp-archive`.

Leave the database alone. WordPress will not run from `_wp-archive` (its
configured site URL is the root), which is the intent — it is cold storage, not
a working install. Keep it until you are confident in the new site, then delete
the folder and drop the database.

> The old `.htaccess` at the root is WordPress's rewrite block. It gets replaced
> in Step 3 — that is why it moves into `_wp-archive` rather than staying.

---

## Step 2 — Move the static files up

1. Double-click into `public_html/2026`.
2. **Select All** (top toolbar), then click **Move**.
3. In the path box, change `/public_html/2026` to `/public_html` and confirm.

Everything lands in the root: the 15 `.html` files, `assets/`, `sitemap.xml`,
`robots.txt`, `favicon.ico`, and the images.

Watch for two things:

- **Hidden files.** Click **Settings → Show Hidden Files (dotfiles)** before
  Select All, or a `.htaccess` inside `2026` will be left behind.
- **A name collision** with a placeholder `index.html` still at the root
  (Case A). Delete the placeholder first so the move does not stall.

Then go back up and delete the now-empty `2026` folder.

---

## Step 3 — Install the root `.htaccess`

Upload the `.htaccess` from this repo into `public_html`. In File Manager:
**Upload**, pick the file, and let it overwrite.

If the upload is blocked because the name starts with a dot, create it instead:
**+ File**, name it `.htaccess`, then right-click → **Edit** and paste the
contents.

This is what 301-redirects the old `/2026/…` URLs to the root, so any link
already shared or indexed still resolves.

`build.py` only overwrites the files it generates by name — it never clears the
directory — so re-running the build will not remove this `.htaccess`.

---

## Step 4 — Verify

Your hosts entry (`68.66.200.215 bishopandadkins.com`) points your machine at
this server already, so you can check before public DNS matters. Hard-reload
(Ctrl+Shift+R / Cmd+Shift+R) — the old site will be cached.

- `https://bishopandadkins.com/` → the new home page
- `https://bishopandadkins.com/about.html` → loads, styled, images present
- `https://bishopandadkins.com/2026/about.html` → **301** to
  `https://www.bishopandadkins.com/about.html`
- `https://bishopandadkins.com/no-such-page` → the custom 404

Add `www.bishopandadkins.com` to your hosts entry too, since the `.htaccess`
canonicalizes to `www` — otherwise that redirect sends you to the live public
site instead of this server:

```
68.66.200.215  bishopandadkins.com www.bishopandadkins.com
```

Check the browser console (F12) for 404s on CSS, JS, or images. There should be
none — but that is where a missed file from Step 2 shows up.

---

## Step 5 — After it is live

- **Google Search Console** — submit `https://www.bishopandadkins.com/sitemap.xml`.
  The 301s tell Google the `/2026/` URLs moved; no manual removal needed.
- **Remove the hosts entry** from your machine once public DNS is correct,
  otherwise you will keep seeing this server even if DNS later changes.
- The `.htaccess` forces `https` and `www`. Confirm the SSL certificate covers
  both `bishopandadkins.com` and `www.bishopandadkins.com` (cPanel → **SSL/TLS
  Status**), or the `www` redirect will land on a certificate warning.

---

## Still open before this is a real launch

Carried over from `README.md` — none of these block the move, but they are all
visible to a client on the live site:

- `PORTAL_URL` and `PAYMENT_URL` in `build.py` are still `#`.
- The contact form is markup only; it posts nowhere.
- Home-page testimonials are placeholders, not real client quotes.
- Bios for Cathy Davis, Lorie Zimmer, Stephanie Powers, and Gina Blair are
  role-level placeholders.
