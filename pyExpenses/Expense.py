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

    def addItem(self, time, baserec):
        self.rec_m.addItem(time, baserec)
        Config.setDefaultType(baserec)

    def figure_out(self, begin, end, parsers = []):
        """
        """
        starttime = time.time()
        
        data = self.rec_m.date_range(begin, end)
        parser = RP.MainParser(data)
        parser.extend(parsers)
        return parser.parse()
        
    def importData(self, filename):
        self.rec_m.importRecord(filename)

    def exportData(self, filename):
        self.rec_m.exportRecord(filename)
