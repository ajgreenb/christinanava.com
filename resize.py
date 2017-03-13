import os
import re
import shutil

from PIL import Image
LANCZOS = Image.LANCZOS

from generate import is_image

full_width = 1500
mobile_width = 900
thumb_width = 400

def has(expr, lst):
    """
    Searches a list of strings to see if one matches the passed regex.
    """

    for o in lst:
        if re.search(expr, o) is not None:
            return True
    return False

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    Adapted from the Django project.
    """

    value = re.sub(r'[^\w\s_]', '', value).strip().lower()
    value = re.sub(r'[_\s]+', '_', value)
    return value

MEDIA_DIR = 'media'
PROCESSED_DIR = '.' + MEDIA_DIR

def ignore(path, names):
    """
    Helper function for `shutil.copytree` that avoids copying any files other
    than the top-level ones from the `media` directory.
    """

    if path == MEDIA_DIR: return []
    return filter(lambda n: os.path.isfile(os.path.join(path, n)), names)

# Clean up and regenerate processed media-file directory.
if os.path.isdir(PROCESSED_DIR):
    shutil.rmtree(PROCESSED_DIR)
shutil.copytree(MEDIA_DIR, PROCESSED_DIR, ignore = ignore)

for dirpath, dirnames, filenames in os.walk(MEDIA_DIR):

    # Ignore PNGs in the top-level directory; these don't need to be full-size
    # and thus resized.
    if dirpath == MEDIA_DIR: continue

    # Filter any possible non-image files.
    pngs = filter(is_image, filenames)

    # Iterate over each full-sized PNG to resize it.
    for png_name in pngs:

        name, _ = os.path.splitext(png_name)
        name = slugify(name)

        # Path to full-sized image.
        png_path = os.path.join(dirpath, png_name)

        print 'Resizing {}...'.format(png_path)
        with Image.open(png_path) as img:

            orig_width, orig_height = img.size

            full_path   = '.' + os.path.join(dirpath, name + '-{0}x{1}.png')
            mobile_path = '.' + os.path.join(dirpath, name + '-{0}x{1}.mobile.png')
            thumb_path  = '.' + os.path.join(dirpath, name + '.thumb.png')

            # Resize over-sized images.
            if orig_width > full_width:
                full_height = int(round(orig_height * full_width / orig_width))
                full = img.resize((full_width, full_height), LANCZOS)
                full.save(full_path.format(full_width, full_height))
                full.close()
            else:
                img.save(full_path.format(orig_width, orig_height))

            # Generate smaller images for mobile phones.
            if orig_width > mobile_width:
                mobile_height = int(round(orig_height * mobile_width / orig_width))
                mobile = img.resize((mobile_width, mobile_height), LANCZOS)
                mobile.save(mobile_path.format(mobile_width, mobile_height))
                mobile.close()
            else:
                img.save(mobile_path.format(orig_width, orig_height))

            # Generate thumbnail-sized copies of each image.
            if orig_width > thumb_width:
                thumb_height = int(round(orig_height * thumb_width / orig_width))
                # Thumbnail method resizes the image in place.
                img.thumbnail((thumb_width, thumb_height), LANCZOS)
                img.save(thumb_path)
            else:
                img.save(thumb_path)
