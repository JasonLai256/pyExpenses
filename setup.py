#!/usr/bin/env python

import os
from setuptools import setup
from pyExpenses import __version__


setup(name='pyExpenses',
      version=__version__,
      description='pyExpenses is a python package for simply personal financial management.',
      author='Jason Lai',
      author_email='jasonlai256@gmail.com',
      maintainer='Jason Lai',
      maintainer_email='jasonlai256@gmail.com',
      url='https://github.com/JasonLai256/pyExpenses.git',
      packages=['pyExpenses'],
      license="BSD",
      platforms=["any"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Office/Business :: Financial',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
 )
