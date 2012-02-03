#! /usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import date, timedelta

from RecManipImpl import *


class RecManip(object):
    def __init__(self, **kwargs):
        self.impl = PickleImpl(**kwargs)

    def addItem(self, time, base_rec):
        """add a basic record to storage."""
        self.impl.addItem(time, base_rec)

    def delItem(self, date, base_rec):
        """delete a specified record.
        @NOTE: if date not exist,raise a exception.
        """
        self.impl.delItem(date, base_rec)

    def updateItem(self, date, base_rec, new_rec):
        self.impl.updateItem(date, base_rec, new_rec)

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