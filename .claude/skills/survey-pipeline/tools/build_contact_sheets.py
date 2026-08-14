#!/usr/bin/env python3
"""Contact-sheet builder for the survey compilation-figure pipeline (topic-agnostic).

Walks a directory of scraped candidate images (one subdirectory per source paper) and renders
labelled CONTACT SHEETS -- a grid, ~24 tiles/sheet, each tile stamped with a global INDEX and its
<subdir>/<filename> -- plus a manifest TSV. A vision pass then Reads each sheet and classifies
every tile into {subject-present, results-plot, neither}; the 'neither' tiles are PURGED from the
pool before any compilation figure is built (see /survey-audit auditor 6, and
.claude/memory/scraped_asset_subject_audit.md).

Usage:
    python3 build_contact_sheets.py <image_dir> <out_dir> [--per 24] [--cols 6]

Outputs:
    <out_dir>/sheet_NN.png        labelled contact sheets
    <out_dir>/img_manifest.tsv    idx <TAB> key <TAB> filename <TAB> sheet   (one row per image)

Then, per sheet, write a classification row per tile: idx <TAB> class <TAB> path
(class in {subject|plot|neither}); move every 'neither' out of <image_dir> and keep a purge log.
"""
import os, sys, math, argparse
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None

EXT = (".png", ".jpg", ".jpeg")

def load_font(sz, bold=True):
    cands = (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if bold else
             ["/System/Library/Fonts/Supplemental/Arial.ttf"]) + \
            ["/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for p in cands:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image_dir"); ap.add_argument("out_dir")
    ap.add_argument("--per", type=int, default=24); ap.add_argument("--cols", type=int, default=6)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)

    imgs = []
    for key in sorted(os.listdir(a.image_dir)):
        d = os.path.join(a.image_dir, key)
        if not os.path.isdir(d): continue
        for fn in sorted(os.listdir(d)):
            if fn.lower().endswith(EXT):
                imgs.append((key, fn, os.path.join(d, fn)))
    if not imgs:
        sys.exit(f"no images under {a.image_dir}")

    fbig, fcap = load_font(26), load_font(15, bold=False)
    cols, rows = a.cols, math.ceil(a.per / a.cols)
    IW, IH, CAPH, PAD = 258, 190, 40, 8
    TW, TH = IW, IH + CAPH
    manifest = ["idx\tkey\tfilename\tsheet"]
    nsheets = math.ceil(len(imgs) / a.per)
    for s in range(nsheets):
        chunk = imgs[s*a.per:(s+1)*a.per]
        W = cols*TW + (cols+1)*PAD
        H = rows*TH + (rows+1)*PAD + 34
        sheet = Image.new("RGB", (W, H), "#1a1a1a"); dr = ImageDraw.Draw(sheet)
        dr.text((PAD, 6), f"CONTACT SHEET {s+1}/{nsheets}  (tiles {s*a.per}-{s*a.per+len(chunk)-1})",
                fill="white", font=fbig)
        for i, (key, fn, path) in enumerate(chunk):
            idx = s*a.per + i; r, c = divmod(i, cols)
            x = PAD + c*(TW+PAD); y = 34 + PAD + r*(TH+PAD)
            try:
                im = Image.open(path).convert("RGB"); im.thumbnail((IW, IH))
                sheet.paste(Image.new("RGB", (IW, IH), "#333"), (x, y))
                sheet.paste(im, (x + (IW-im.width)//2, y + (IH-im.height)//2))
            except Exception as e:
                dr.rectangle([x, y, x+IW, y+IH], fill="#552222")
                dr.text((x+4, y+4), str(e)[:30], fill="white", font=fcap)
            dr.rectangle([x, y+IH, x+IW, y+IH+CAPH], fill="#000")
            dr.rectangle([x, y, x+54, y+30], fill="#e8b400")
            dr.text((x+5, y+2), str(idx), fill="black", font=fbig)
            cap = fn if len(fn) <= 26 else fn[:12] + ".." + fn[-11:]
            dr.text((x+4, y+IH+3), key, fill="#8fd6ff", font=fcap)
            dr.text((x+4, y+IH+20), cap, fill="#dddddd", font=fcap)
            manifest.append(f"{idx}\t{key}\t{fn}\t{s+1}")
        out = os.path.join(a.out_dir, f"sheet_{s+1:02d}.png")
        sheet.save(out); print("wrote", out, sheet.size)
    open(os.path.join(a.out_dir, "img_manifest.tsv"), "w").write("\n".join(manifest) + "\n")
    print(f"{len(imgs)} images across {nsheets} sheets; wrote img_manifest.tsv")

if __name__ == "__main__":
    main()
