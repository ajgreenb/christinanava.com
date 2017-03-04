#!/usr/bin/env python
# clean.py
#
# Prunes any unused files from the _site directory, to prevent uploading them
# to the website.

import os
import sys

SITE = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), '_site')

print 'Pruning crufty files...'

for dirpath, dirnames, filenames in os.walk(SITE):
    if '.DS_Store' in filenames:
        os.remove(os.path.join(dirpath, '.DS_Store'))
