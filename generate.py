import itertools
import mimetypes
import os
import shutil

from PIL import Image
from jinja2 import Environment, FileSystemLoader

SITE_PATH = '_site'
PAGE_PATH = 'pages'
MEDIA_PATH = '.media'
PAGES = [ 'index.html', 'photo.html', 'research.html', 'motion.html', 'about.html' ]

def listdir(d):
    return [ os.path.join(d, e) for e in os.listdir(d) ]

def is_image(path):
    mime, _ = mimetypes.guess_type(path)
    return mime.startswith('image/') if mime is not None else False

def sort_tuple(s):
    if 'thumb' in s: return 2
    if 'mobile' in s: return 1
    return 0

def sort_tuples_by_name(s):
    s = os.path.basename(s[0])
    return s.split('-')[0]

def get_images(section):
    image_dir = os.path.join(MEDIA_PATH, section)
    image_paths = filter(is_image, listdir(image_dir))
    image_paths = [ ip[1:] for ip in image_paths ]
    keyfunc = lambda s: os.path.basename(s).split('.')[0].split('-')[0]
    tuples = [ sorted(list(g), key = sort_tuple) for k, g in itertools.groupby(image_paths, keyfunc) ]
    return sorted(tuples, key = sort_tuples_by_name)

def get_photo_images():
    retval = {}
    rootdir = os.path.join(MEDIA_PATH, 'photo')
    subcategories = os.listdir(rootdir)
    for subcat in subcategories:
        retval[subcat] = get_images('photo/' + subcat)

    return retval

def build_site():

    if os.path.isdir(SITE_PATH):
        shutil.rmtree(SITE_PATH)

    os.mkdir(SITE_PATH)

    # Copy static files to _site.
    shutil.copytree(MEDIA_PATH, os.path.join(SITE_PATH, 'media'))
    shutil.copytree('assets', os.path.join(SITE_PATH, 'assets'))

    loader = FileSystemLoader('./templates')
    env = Environment(loader = loader)

    env.globals = {
        'breakpoint': '40em',
    }

    index = env.get_template('index.html').render()
    with open(os.path.join(SITE_PATH, 'index.html'), 'w') as p:
        p.write(index)

    images = get_photo_images()
    content = env.get_template('photo.html').render(images = images, section = 'photo')
    with open(os.path.join(SITE_PATH, 'photo.html'), 'w') as f:
        f.write(content)

    images = get_images('research')
    content = env.get_template('research.html').render(images = images, section = 'research')
    with open(os.path.join(SITE_PATH, 'research.html'), 'w') as f:
        f.write(content)

    images = get_images('motion')
    content = env.get_template('motion.html').render(images = images, section = 'motion')
    with open(os.path.join(SITE_PATH, 'motion.html'), 'w') as f:
        f.write(content)

    content = env.get_template('about.html').render(section = 'about')
    with open(os.path.join(SITE_PATH, 'about.html'), 'w') as f:
        f.write(content)

if __name__ == '__main__':
    build_site()
