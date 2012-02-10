#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
    pyExpenses.RecManip
    ~~~~~~~~~~~~~~~~~~~

    Implements the interface's object that manipulator of records for pyExpenses.

    :copyright: (c) 2012 by Jason Lai.
    :license: BSD, see LICENSE for more details.
"""

from datetime import date, timedelta

from ConfigManip import Config
import RecManipImpl

STORAGE_BACKEND = RecManipImpl.__dict__[Config.getInfo('StorageBackend')]

class RecManip(object):

    def setUp(self, *args, **kwargs):
        """It's the method really initialize the instance. This should be
        called after create a instance, the passing arguments can control
        defferent options.
        """
        self.impl = STORAGE_BACKEND(*args, **kwargs)

    def updatePassword(self, oldpwd, newpwd):
        self.impl.updatePassword(oldpwd, newpwd)

    def cancelPassword(self, oldpwd):
        from RecManipImpl import DEFAULT_PASSWORD
        self.impl.updatePassword(oldpwd, DEFAULT_PASSWORD)

    def addItem(self, rdate, base_rec):
        """add a basic record to storage."""
        self.impl.addItem(rdate, base_rec)

    def delItem(self, rdate, base_rec):
        """delete a specified record.
        @NOTE: if date not exist,raise a exception.
        """
        self.impl.delItem(rdate, base_rec)

    def updateItem(self, rdate, base_rec, new_rec):
        self.impl.updateItem(rdate, base_rec, new_rec)

    def getAll(self):
        return self.impl.getAll()

    def getInfo(self):
        return self.impl.getInfo()

    def date_range(self, begin, end):
        """Return a range of records in specified period.
        @NOTE:
        """
        return self.impl.date_range(begin, end)

    def findDate(self, fdate):
        """find and return the matching record. 
        @NOTE: if date not exist,raise a exception.
        """
        return self.impl.date_range(fdate, fdate + timedelta(1))

    def findDates(self, fdate, nth=0):
        return self.impl.date_range(fdate, fdate + timedelta(nth))

    def clear(self):
        """clear all the data in data manipulator."""
        self.impl.clear()

    def save(self):
        """save all the data in data manipulator to permanent storage."""
        self.impl.save()

    def importRecord(self, filename):
        self.impl.importRecord(filename)

    def exportRecord(self, filename):
        self.impl.exportRecord(filename)
