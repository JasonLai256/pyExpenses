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
import Projects
import RecParser as RP
import ErrorHandle as EH


class Expense(object):
    def __init__(self):
        self.rec_m = RecManip()    # Records Manipulator
        self.projects = {}
        self.isSetup = False

    def __getattribute__(self, name):
        """If isSetup attribute was False, when get a attributes of
        Expense's instance will raise AttributeError except setUp,
        addRecord and isSetup three attributes.
        @Note: Should call setUp method to avoid AttributeError.
        """
        if not name.startswith('__') and \
        not name.startswith('_') and \
        name not in ('setUp', 'addRecord', 'isSetup', 'rec_m', 'projects') and \
        not self.isSetup:
            raise AttributeError

        return super(Expense, self).__getattribute__(name)

    def setUp(self, rmArgs={}):
        """It's the method setup the Expense's instance, this should be
        called after initialise finish. 
        """
        self.rec_m.setUp(**rmArgs)
        
        self.isSetup = True
        self._setUpProjects()
        self._setUpRecords()

    def addRecord(self, rdate, baserec):
        if self.isSetup:
            self.rec_m.addItem(rdate, baserec)
            Config.setDefault(baserec)
        else:
            buf = record2buf(rdate, baserec)
            recbuf = Config.getRecordBuffer()
            recbuf.append(buf)
            Config.setRecordBuffer(recbuf)

    def deleteRecord(self, rdate, baserec):
        self.rec_m.delItem(rdate, baserec)

    def updateRecord(self, rdate, baserec, updaterec):
        self.rec_m.updateItem(rdate, baserec, updaterec)

    def listProject(self, ptype=None):
        if not ptype:
            return self.projects.iteritems()
        else:
            return (
                (name, proj)
                    for name, proj in self.projects.iteritems()
                        if proj.p_type == ptype
            )
        
    def addProject(self, name, project):
        if self.projects.has_key(name):
            return False
        self.projects[name] = project
        return True

    def deleteProject(self, name):
        del self.projects[name]

    # def sumOfAmount(self):
    #     pass

    def figureOutRecords(self, begin, end, parsers = []):
        """
        """
        data = self.rec_m.date_range(begin, end)
        parser = RP.MainParser(data)
        parser.extend(parsers)
        return parser.parse()
    
    def saveProjects(self):
        # savebuf = {}
        # for name, proj in self.projects.items():
        #     savebuf[name] = proj.export_to_dict()
        #     savebuf[name]['projtype'] = proj.__class__.__name__
        # Config.setProjectBuffer(savebuf)
        pass

    def saveRecords(self):
        self.rec_m.save()

    def save(self):
        self.saveProjects()
        self.saveRecords()
                
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

    def _setUpProjects(self):
        # projbuf = Config.getProjectBuffer()
        # for name, dictbuf in projbuf.items():
        #     projtype = dictbuf['projtype']()
        #     proj = Projects.__dict__[projtype]
        #     self.projects[name] = proj.import_from_dict(dictbuf)
        pass

    def _setUpRecords(self):
        recbuf = Config.getRecordBuffer()
        for buf in recbuf:
            rdate, rec = buf2record(buf)
            self.addRecord(rdate, rec)
        # set record buffer up to default value a empty list.
        Config.setRecordBuffer(list())

    def _checkProjects(self, rdate, baserec, newrec=None, act='add'):
        for proj in self.projects:
            if proj.p_type == 'statistic':
                proj.register(rdate, baserec, newrec, act)

