#!usr/bin/env python
# -*- coding:utf-8 -*-

import os

logfile = os.path.join(os.getcwd(), 'errors.LOG')
    
def valueError(estring):
    raise ValueError(estring)

def ioError(estring):
    raise IOError(estring)

def indexError(estring):
    raise IndexError(estring)
