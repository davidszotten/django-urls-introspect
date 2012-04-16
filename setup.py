#!/usr/bin/env python
"""
django urls introspect
======

Experimental tool to introspect django urls and highlight views where the
signature doesn't match the keywords captured in the url. See
http://www.szotten.com/david/introspecting-django-urls-for-fun-and-profit.html
for (a little) more info.

copyright (c) 2012 by David Szotten
license: MIT. See LICENSE for details
"""

from setuptools import setup

setup(
    name='django-urls-introspect',
    version='0.1.0',
    author='David Szotten',
    author_email='Author name (as one word) at gmail.com',
    url='https://github.com/davidszotten/django-urls-introspect',
    description='An (experimental) tool for finding bugs in django url patterns',
    long_description=__doc__,
    install_requires=['django>=1.2,<1.4'],
    license='MIT',
    zip_safe=False,
)
