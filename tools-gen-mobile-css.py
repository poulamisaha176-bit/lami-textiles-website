#!/usr/bin/env python3
"""Generate mobile overrides as real classes.

Matching on [style*="..."] does not survive site.js touching an element: the
browser re-serialises the whole style attribute the moment any property is set
on it, so the authored substring disappears. Instead, every element needing a
mobile treatment gets a generated class, and the stylesheet targets that.
Identical treatments share one class.
"""
import pathlib, re, collections

ROOT = pathlib.Path("/home/user/lami-textiles-website")
HTML = sorted(ROOT.glob("*.html"))

classes = {}          # css body -> class name
order = []


def cls_for(body):
    if body not in classes:
        name = f"m{len(classes) + 1}"
        classes[body] = name
        order.append((name, body))
    return classes[body]


def px(v):
    return f"{int(round(v))}px"


def overrides(style):
    """Mobile counterpart for one inline style string, or None."""
    out = []
    big_type = False

    m = re.search(r"font:\s*(\d+)\s+(\d+)px", style)
    if m:
        size = int(m.group(2))
        if size >= 28:
            out.append(f"font-size:{px(max(20, size * 0.62))}")
            if size >= 44:
                big_type = True

    m = re.search(r"(?<!-)\bpadding:\s*((?:-?\d+px\s*)+)(?=;|$)", style)
    if m:
        vals = [int(x[:-2]) for x in m.group(1).split()]
        if any(v >= 40 for v in vals):
            if len(vals) == 1:
                nv = [max(16, vals[0] * 0.55)]
            elif len(vals) == 2:
                nv = [vals[0] * 0.55, min(vals[1], 20)]
            elif len(vals) == 3:
                nv = [vals[0] * 0.55, min(vals[1], 20), vals[2] * 0.55]
            else:
                nv = [vals[0] * 0.55, min(vals[1], 20),
                      vals[2] * 0.55, min(vals[3], 20)]
            out.append("padding:" + " ".join(px(v) for v in nv))

    m = re.search(r"\bmin-height:\s*(\d+)px", style)
    if m and int(m.group(1)) >= 400:
        out.append(f"min-height:{px(max(240, int(m.group(1)) * 0.5))};height:auto")
    else:
        m = re.search(r"(?<!-)\bheight:\s*(\d+)px", style)
        if m and int(m.group(1)) >= 400:
            out.append(f"height:{px(max(240, int(m.group(1)) * 0.5))}")

    m = re.search(r"\bgap:\s*(\d+)px", style)
    if m and int(m.group(1)) >= 28:
        out.append(f"gap:{px(int(m.group(1)) * 0.5)}")

    if "grid-template-columns" in style:
        out.append("grid-template-columns:1fr")

    if re.search(r"height:\s*92vh", style):
        out.append("height:64vh")

    return (";".join(out), big_type) if out else (None, False)


total = 0
for path in HTML:
    src = path.read_text(encoding="utf-8")

    def repl(mo):
        global total
        style = mo.group(1)
        body, big = overrides(style)
        if not body:
            return mo.group(0)
        names = [cls_for(body)]
        if big:
            names.append("mxl")
        total += 1
        return f'class="{" ".join(names)}" style="{style}"'

    src = re.sub(r'style="([^"]*)"', repl, src)
    path.write_text(src, encoding="utf-8")

rules = "\n".join(f"  .{n} {{ {b.replace(';', ' !important; ')} !important; }}"
                  for n, b in order)

css = f"""/* Mobile layout for lami textiles.

   The design tool emitted every rule inline, which outranks any stylesheet.
   These overrides therefore carry !important, and hang off generated classes
   rather than matching the inline text — site.js rewrites style attributes at
   runtime, which would break substring matching.

   Generated from the markup by scratchpad/gencss2.py.
   Desktop is untouched: everything sits inside a max-width query. */

/* No overflow-x:hidden here on purpose — it silently breaks position:sticky,
   which the inner-page nav relies on. Overflow is fixed at the cause instead. */
img {{ max-width:100%; }}

@media (max-width:820px) {{

  /* Nav: let the links wrap beneath the wordmark instead of overflowing. */
  [data-nav] {{
    padding:14px 20px !important;
    flex-wrap:wrap !important;
    gap:10px 16px !important;
  }}
  [data-navlinks] {{
    flex-wrap:wrap !important;
    gap:12px 18px !important;
    font-size:13px !important;
    width:100% !important;
  }}

  /* Home hero: four side-by-side panels become a vertical stack. */
  [data-panels] {{ flex-direction:column !important; height:auto !important; }}
  [data-panels] > a {{
    min-height:68vh !important;
    border-left:none !important;
    border-top:1px solid rgba(250,248,243,.25) !important;
  }}
  [data-panels] > a:first-child {{ border-top:none !important; }}

  /* Hero caption is inset to the desktop gutter; pull in and stack. */
  [data-hero-cap] {{
    left:20px !important;
    right:20px !important;
    bottom:24px !important;
    flex-direction:column !important;
    align-items:flex-start !important;
    gap:10px !important;
  }}

  /* Generated per-element overrides. */
{rules}
}}

/* Narrow phones: rein the display type in a little further. */
@media (max-width:420px) {{
  .mxl {{ font-size:27px !important; }}
  [data-panels] > a {{ min-height:58vh !important; }}
}}
"""

(ROOT / "site.css").write_text(css, encoding="utf-8")
print(f"{total} elements classed, {len(order)} distinct classes")
