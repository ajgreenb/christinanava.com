# import mimetypes
import os
import shutil

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

    for page in PAGES:
        content = env.get_template(page).render()
        with open(os.path.join(SITE_PATH, page), 'w') as p:
            p.write(content)


if __name__ == '__main__':
    build_site()
