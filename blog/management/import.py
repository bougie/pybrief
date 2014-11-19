#!/usr/bin/env python
import os
import sys
base_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pybrief.settings")
django.setup()

import fnmatch
from blog.utils import parse_blog_file
from blog.forms import PostForm


def main():
    path = os.path.join(base_dir, 'data')
    for item in os.listdir(path):
        filename = os.path.join(path, item)
        if fnmatch.fnmatch(filename, '*.bp'):
            bpcontent = parse_blog_file(filename)
            if bpcontent is not None:
                try:
                    PostForm(bpcontent).save()
                except Exception as e:
                    print(str(e))
            else:
                return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
