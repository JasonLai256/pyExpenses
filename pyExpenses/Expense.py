#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
from decimal import Decimal
from datetime import date

from RecManip import RecManip
from ConfigManip import Config
import RecParser as RP
import ErrorHandle as EH


class Expense(object):
    def __init__(self):
        self.rec_m = RecManip()    # Records Manipulator
        self.projects = []
        self.isSetup = False

    def setUp(self, rmArgs={}):
        """It's the method setup the Expense's instance, this should be
        called after initialise finish.
        """
        self.rec_m.setUp(**rmArgs)
        # ......
        self.isSetup = True

    def addRecord(self, rdate, baserec):
        self.rec_m.addItem(time, baserec)
        Config.setDefaultType(baserec)

    def deleteRecord(self, rdate, baserec):
        pass

    def updeteRecord(self, rdate, baserec, updaterec):
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
