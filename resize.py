import os
import re

from PIL import Image

thumbnail_width = 400

for dirpath, dirnames, filenames in os.walk('media'):

    # Ignore PNGs in the top-level directory; these don't need to be full-size
    # and thus resized.
    if dirpath == 'media': continue

    # Parse out full-sized images (exclude thumbnails.)
    pngs = filter(lambda f: re.search(r'(?<!thumb).png$', f), filenames)

    # Iterate over each full-sized PNG to resize it.
    for png_path in pngs:

        name, _ = os.path.splitext(png_path)

        # If a thumbnail already exists for it, skip.
        if name + '.thumb.png' in filenames: continue

        # Relative path to full-sized image.
        full_path = os.path.join(dirpath, png_path)

        # Relative path to thumbnail image.
        full_thumb_path = os.path.join(dirpath, '{}.thumb.png'.format(name))

        with Image.open(full_path) as img:
            width, height = img.size
            thumbnail_height = round(height * thumbnail_width / width)
            print 'Resizing {}...'.format(png_path)
            img.thumbnail((thumbnail_width, thumbnail_height), Image.LANCZOS)
            img.save(full_thumb_path)
