import mimetypes
import os

import boto3

SITE_DIR = '_site'
s3 = boto3.client('s3')

def is_woff(path):
    return path.endswith('woff') or path.endswith('woff2')

for dirpath, dirnames, filenames in os.walk(SITE_DIR):
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        key = path.replace(SITE_DIR + '/', '')
        mime, _ = mimetypes.guess_type(path)
        if mime is None:
            if is_woff(path):
                mime = 'application/x-font-woff'
            else:
                raise Exception('Could not guess Content-Type for: ' + path)
        print 'Uploading {}...'.format(key)
        s3.upload_file(path, 'christinanava.com', key, ExtraArgs = {
            'ContentType': mime,
            'ACL': 'public-read',
        })
