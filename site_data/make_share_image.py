#!/usr/bin/env python3
"""
Make the site's share (preview) image, assets/share-image.jpg, from a photo.

Usage: python3 site_data/make_share_image.py PHOTO [FOCUS_X FOCUS_Y]

Crops the photo to 1200 x 630 (the shape Facebook, LinkedIn, X and messaging
apps use for link previews), keeping the point FOCUS_X, FOCUS_Y (fractions of
the width and height, default 0.5 0.5 = the centre) as near the middle as the
crop allows, and saves a JPEG of about 100-250 KB. Then run generate_site.py:
the og:image tags appear on every page once this file exists.
Needs Pillow (pip install pillow).
"""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from common import SITE, SHARE_IMAGE

W, H = 1200, 630

def main():
    src = sys.argv[1]
    fx = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    fy = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    scale = max(W / sw, H / sh)
    cw, ch = W / scale, H / scale            # crop box size in source pixels
    left = min(max(fx * sw - cw / 2, 0), sw - cw)
    top = min(max(fy * sh - ch / 2, 0), sh - ch)
    out = im.crop((round(left), round(top), round(left + cw), round(top + ch))).resize((W, H), Image.LANCZOS)
    dest = os.path.join(SITE, SHARE_IMAGE)
    out.save(dest, "JPEG", quality=85, optimize=True, progressive=True)
    print(f"Wrote {dest} ({os.path.getsize(dest) // 1024} KB) from {sw}x{sh} source")

if __name__ == "__main__":
    main()
