# LAMI Textiles

Portfolio site for LAMI Textiles — biodegradable materials made from fish-scale waste.

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

## Images

Every image lives in `assets/` and is referenced with a lowercase, hyphenated
filename. Avoid spaces, capitals and parentheses in filenames — they have to be
URL-encoded and break easily across servers.

Export images at roughly 2000px on the long edge and compress them before
committing. The originals are large, and page weight is what visitors feel most
on a phone.
