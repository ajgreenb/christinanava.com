# import mimetypes
import os
import shutil

from PIL import Image
from jinja2 import Environment, FileSystemLoader

SITE_PATH = '_site'
PAGE_PATH = 'pages'
MEDIA_PATH = 'media'
PAGES = [ 'index.html', 'photo.html', 'research.html', 'motion.html' ]

def listdir(d):
    return [ os.path.join(d, e) for e in os.listdir(d) ]

# def is_image(path):
#     mime, _ = mimetypes.guess_type(path)
#     return mime.startswith('image/')

def by_number(path):
    path = os.path.basename(path)
    return int(path.split('.')[0])

def get_images(section):
    image_dir = os.path.join(MEDIA_PATH, section)
    image_paths = listdir(image_dir)
    image_paths = filter(lambda p: 'thumb' not in p, image_paths)
    image_paths.sort(key = by_number)
    tuples = []
    for ip in image_paths:
        fname, _ = os.path.splitext(ip)
        with Image.open(ip) as img:
            width, height = img.size
            tuples.append((fname, width, height))

    return tuples

def build_site():

    if os.path.isdir(SITE_PATH):
        shutil.rmtree(SITE_PATH)

    os.mkdir(SITE_PATH)

    # Copy static files to _site.
    shutil.copytree('media', os.path.join(SITE_PATH, 'media'))
    shutil.copytree('assets', os.path.join(SITE_PATH, 'assets'))

    loader = FileSystemLoader('./templates')
    env = Environment(loader = loader)

    env.globals = {
        'breakpoint': '40em',
    }

    index = env.get_template('index.html').render()
    with open(os.path.join(SITE_PATH, 'index.html'), 'w') as p:
        p.write(index)

    images = get_images('research')
    research = env.get_template('research.html').render(images = images)
    with open(os.path.join(SITE_PATH, 'research.html'), 'w') as p:
        p.write(research)


if __name__ == '__main__':
    build_site()
