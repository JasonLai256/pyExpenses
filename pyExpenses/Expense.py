#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
from decimal import Decimal
from datetime import date

from RecManip import RecManip
from ConfigManip import Config
from utils import buf2record, record2buf
import RecParser as RP
import ErrorHandle as EH


class Expense(object):
    def __init__(self):
        self.rec_m = RecManip()    # Records Manipulator
        self.projects = []
        self.isSetup = False

    def __getattribute__(self, name):
        """If isSetup attribute was False, when get a attributes of
        Expense's instance will raise AttributeError except setUp,
        addRecord and isSetup three attributes.
        @Note: Should call setUp method to avoid AttributeError.
        """
        if not name.startswith('__') and \
        name not in ('setUp', 'addRecord', 'isSetup', 'rec_m') and \
        not self.isSetup:
            raise AttributeError

        return super(Expense, self).__getattribute__(name)

    def setUp(self, rmArgs={}):
        """It's the method setup the Expense's instance, this should be
        called after initialise finish. 
        """
        self.rec_m.setUp(**rmArgs)
        
        self.isSetup = True
        recbuf = Config.getRecordBuffer()
        for buf in recbuf:
            rdate, rec = buf2record(buf)
            self.addRecord(rdate, rec)
        # set record buffer up to default value a empty list.
        Config.setRecordBuffer(list())

    def addRecord(self, rdate, baserec):
        # if self.isSetup:
        #     self.rec_m.addItem(rdate, baserec)
        #     Config.setDefaultType(baserec)
        # else:
            pass

    def deleteRecord(self, rdate, baserec):
        pass

    def updateRecord(self, rdate, baserec, updaterec):
        pass

    def figure_out(self, begin, end, parsers = []):
        """
        """
        data = self.rec_m.date_range(begin, end)
        parser = RP.MainParser(data)
        parser.extend(parsers)
        return parser.parse()
        
    def importData(self, filename):
        """import a backup file that was implemented by CSV format from 
        specify file, note that it will override original data."""
        self.rec_m.importRecord(filename)

    def exportData(self, filename):
        """Export textual data records that is implemented by CSV format
        into the specified file.
        """
        self.rec_m.exportRecord(filename)

    def resetAll(self):
        """This method reset all the data of the Expense to default status.
        Be careful when call this method, it should be make a warning
        message to the user.
        """
        pass
