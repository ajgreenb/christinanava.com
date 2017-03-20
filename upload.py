import mimetypes
import os
from multiprocessing.pool import ThreadPool

import boto3

SITE_DIR = '_site'
s3 = boto3.client('s3')

def is_woff(path):
    return path.endswith('woff') or path.endswith('woff2')

def upload_file(args):
    filepath, mime = args
    key = filepath.replace(SITE_DIR + '/', '')
    print 'Uploading {}...'.format(key)
    s3.upload_file(
        filepath,
        'aws-website-christinanavacom-zkmp7',
        key,
        ExtraArgs = {
            'ContentType': mime,
            'ACL': 'public-read',
        }
    )


if __name__ == '__main__':

    # Build up a list of files that will be uploaded to Amazon S3.
    to_upload = []

    for dirpath, dirnames, filenames in os.walk(SITE_DIR):
        for filename in filenames:
            if filename == '.DS_Store': continue
            path = os.path.join(dirpath, filename)
            mime, _ = mimetypes.guess_type(path)
            if mime is None:
                if is_woff(path):
                    mime = 'application/x-font-woff'
                else:
                    raise Exception('Could not guess Content-Type for: ' + path)
            to_upload.append((path, mime))

    # Upload site files to S3 in parallel.
    pool = ThreadPool(processes = 10)
    pool.map(upload_file, all_files)
