"""
Resize all images in the 'images' folder by 50%
Run this script in the same folder as your 'images' directory
Install Pillow first: pip install Pillow
Then run: python resize_images.py
"""

from PIL import Image
import os

FOLDER = "images"  # your images folder
QUALITY = 85       # JPEG quality (85 is great balance of size vs quality)

def resize_all(folder):
    count = 0
    skipped = 0
    for root, dirs, files in os.walk(folder):
        for filename in files:
            ext = filename.lower().split('.')[-1]
            if ext not in ('jpg', 'jpeg', 'png', 'webp'):
                continue

            filepath = os.path.join(root, filename)
            try:
                with Image.open(filepath) as img:
                    original_size = os.path.getsize(filepath)
                    orig_w, orig_h = img.size

                    # Skip if already small enough (under 800px wide)
                    if orig_w <= 800:
                        print(f"  SKIP (already small): {filepath} ({orig_w}x{orig_h})")
                        skipped += 1
                        continue

                    new_w = orig_w // 2
                    new_h = orig_h // 2

                    # Use LANCZOS for best quality downscaling
                    resized = img.resize((new_w, new_h), Image.LANCZOS)

                    # Convert RGBA to RGB for JPEGs
                    if ext in ('jpg', 'jpeg') and resized.mode in ('RGBA', 'P'):
                        resized = resized.convert('RGB')

                    # Save back to same path
                    if ext == 'png':
                        resized.save(filepath, 'PNG', optimize=True)
                    else:
                        resized.save(filepath, 'JPEG', quality=QUALITY, optimize=True)

                    new_size = os.path.getsize(filepath)
                    saved_kb = (original_size - new_size) // 1024
                    print(f"  ✓ {filepath}: {orig_w}x{orig_h} → {new_w}x{new_h} | saved {saved_kb}KB")
                    count += 1

            except Exception as e:
                print(f"  ERROR {filepath}: {e}")

    print(f"\n✅ Done! Resized {count} images, skipped {skipped} (already small).")
    print("Now run: git add . && git commit -m 'compress images' && git push")

resize_all(FOLDER)
