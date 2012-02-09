#!/usr/bin/env python

import os
from setuptools import setup
from pyExpenses import __version__

def read(*path):
    return open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *path)).read()


setup(name='pyExpenses',
      version=__version__,
      description='',
      author='Jason Lai',
      author_email='jasonlai256@gmail.com',
      maintainer='Jason Lai',
      maintainer_email='jasonlai256@gmail.com',
      url='',
      packages=['pyExpenses'],
      long_description=read("README.rst"),
      license="",
      platforms=["any"],
 )
