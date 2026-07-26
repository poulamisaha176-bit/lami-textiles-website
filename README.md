# Lami Textiles

Portfolio site for Lami Textiles — biodegradable materials made from fish-scale waste.

## Structure

Plain static HTML, CSS and JavaScript. No build step, no dependencies to install.

| File | Page |
| --- | --- |
| `index.html` | Home |
| `about.html` | About |
| `biomaterials.html` | Biomaterials (material library at `#library`) |
| `bio-sequins.html` | Bio sequins |
| `scale-leather.html` | Scale leather |
| `scale-composites.html` | Scale composites |
| `scale-paper.html` | Scale paper |
| `collaborations.html` | Collaborations |
| `site.js` | Scroll reveals, parallax, hero motion, hover panels |
| `assets/` | All images |
| `.nojekyll` | Stops GitHub Pages running the files through Jekyll |

Page styles are inline in each file's `<head>`, carried over from the original
design export. Fonts (Cormorant Garamond, Archivo) load from Google Fonts.

## Working on it locally

Open `index.html` in a browser, or serve the folder so relative paths behave
exactly as they do in production:

```
python3 -m http.server 8000
```

Then visit http://localhost:8000.

## Publishing

The site deploys from the default branch via GitHub Pages
(**Settings → Pages → Deploy from a branch**). Pushing to that branch updates
the live site within a minute or so.

It is served at https://lami-textiles.com. The `CNAME` file at the repository
root is what tells GitHub Pages which domain to answer on — deleting it drops
the site back to the github.io address, so leave it in place.

DNS is managed at Cloudflare: four `A` records on the apex pointing at GitHub's
Pages addresses, and a `CNAME` on `www` pointing at
`poulamisaha176-bit.github.io`. These records must stay **DNS only** (grey
cloud) rather than proxied, or GitHub cannot renew the HTTPS certificate.

## Images

Every image lives in `assets/` and is referenced with a lowercase, hyphenated
filename. Avoid spaces, capitals and parentheses in filenames — they have to be
URL-encoded and break easily across servers. GitHub Pages is case-sensitive, so
`flatlay.png` and `Flatlay.png` are different files.

The pages expect these 22 files:

```
collab.png              hero-paper.png          presenting.jpeg
composites-b.png        leather-a.png           process-collage.png
composites-c.png        leather-b.png           raw-scales.png
composites.png          leather-face.png        sequin-macro.png
fish-market.png         paper-a.png             sequins-drape.png
flatlay.png             paper-b.png             sequins-held.png
portrait.jpeg           paper-sheet.png         sequins-worn.png
studio-screenprinting.jpeg
```

Export images at roughly 2000px on the long edge and compress them before
committing. The originals are large, and page weight is what visitors feel most
on a phone.
