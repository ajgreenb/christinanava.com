import os
import re
import shutil

from PIL import Image
LANCZOS = Image.LANCZOS

full_width = 1500
mobile_width = 900
thumb_width = 400

def is_original(fname):
    """
    Determines whether a file in a folder is the originally added file
    (and not a resized version.)
    """

    if fname.endswith('.thumb.png'): return False
    if re.match(r'-\d+x\d+\.png$', fname): return False
    if re.match(r'-\d+x\d+\.mobile\.png$', fname): return False
    return True

def has(expr, lst):
    """
    Searches a list of strings to see if one matches the passed regex.
    """

    for o in lst:
        if re.match(expr, o) is not None:
            return True
    return False

MEDIA_DIR = 'media'
PROCESSED_DIR = '.' + MEDIA_DIR
if not os.path.isdir(PROCESSED_DIR):

    def ignore(path, names):
        if path == MEDIA_DIR: return []
        return filter(lambda n: os.path.isfile(os.path.join(path, n)), names)

    shutil.copytree(MEDIA_DIR, PROCESSED_DIR, ignore = ignore)

for dirpath, dirnames, filenames in os.walk(MEDIA_DIR):

    # Ignore PNGs in the top-level directory; these don't need to be full-size
    # and thus resized.
    if dirpath == MEDIA_DIR: continue

    # Parse out full-sized images (exclude thumbnails.)
    pngs = filter(is_original, filenames)

    # Iterate over each full-sized PNG to resize it.
    for png_name in pngs:

        name, _ = os.path.splitext(png_name)

        has_full = has(r'{0}-\d+x\d+\.png$'.format(name), filenames)
        has_mobile = has(r'{0}-\d+x\d+\.mobile\.png$'.format(name), filenames)
        has_thumb = name + '.thumb.png' in filenames

        # If all resized versions already exist, skip this PNG.
        if has_full and has_mobile and has_thumb: continue

        # Path to full-sized image.
        png_path = os.path.join(dirpath, png_name)

        print 'Resizing {}...'.format(png_path)
        with Image.open(png_path) as img:

            orig_width, orig_height = img.size

            full_path   = os.path.join(dirpath, name + '-{0}x{1}.png')
            mobile_path = os.path.join(dirpath, name + '-{0}x{1}.mobile.png')
            thumb_path  = os.path.join(dirpath, name + '.thumb.png')

            if not has_full:
                # Resize over-sized images.
                if orig_width > full_width:
                    full_height = int(round(orig_height * full_width / orig_width))
                    full = img.resize((full_width, full_height), LANCZOS)
                    full.save('.' + full_path.format(full_width, full_height))
                    full.close()
                else:
                    img.save('.' + full_path.format(orig_width, orig_height))

            if not has_mobile:
                # Generate smaller images for mobile phones.
                if orig_width > mobile_width:
                    mobile_height = int(round(orig_height * mobile_width / orig_width))
                    mobile = img.resize((mobile_width, mobile_height), LANCZOS)
                    mobile.save('.' + mobile_path.format(mobile_width, mobile_height))
                    mobile.close()
                else:
                    img.save('.' + mobile_path.format(orig_width, orig_height))


            if not has_thumb:
                # Generate thumbnail-sized copies of each image.
                if orig_width > thumb_width:
                    thumb_height = int(round(orig_height * thumb_width / orig_width))
                    # Thumbnail method resizes the image in place.
                    img.thumbnail((thumb_width, thumb_height), LANCZOS)
                    img.save('.' + thumb_path)
                else:
                    img.save('.' + thumb_path)
