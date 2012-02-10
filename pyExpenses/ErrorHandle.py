#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
    pyExpenses.ErrorHandle
    ~~~~~~~~~~~~~~~~~~~~~~

    Implements the error handle support for pyExpenses.

    :copyright: (c) 2012 by Jason Lai.
    :license: BSD, see LICENSE for more details.
"""

import os

    
def valueError(estring):
    raise ValueError(estring)

def ioError(estring):
    raise IOError(estring)

def indexError(estring):
    raise IndexError(estring)

def attrError(estring):
    raise AttributeError
