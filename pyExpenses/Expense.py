#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
    pyExpenses.Expense
    ~~~~~~~~~~~~~~~~~~

    Implements the schedual object for pyExpenses.

    :copyright: (c) 2012 by Jason Lai.
    :license: BSD, see LICENSE for more details.
"""

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

    def updatePassword(self, oldpwd, newpwd):
        """Update the password of pyExpenses
        """
        self.rec_m.updatePassword(oldpwd, newpwd)

    def cancelPassword(self, oldpwd):
        """Do not use password authentication for pyExpenses
        """
        self.rec_m.cancelPassword(oldpwd)

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
            self._checkProjects(rdate, baserec, act='add')
            Config.setDefault(baserec)
        else:
            buf = record2buf(rdate, baserec)
            recbuf = Config.getRecordBuffer()
            recbuf.append(buf)
            Config.setRecordBuffer(recbuf)

    def deleteRecord(self, rdate, baserec):
        self.rec_m.delItem(rdate, baserec)
        self._checkProjects(rdate, baserec, act='del')

    def updateRecord(self, rdate, baserec, updaterec):
        self.rec_m.updateItem(rdate, baserec, updaterec)
        self._checkProjects(rdate, baserec, updaterec, act='upd')

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

    def allRecords(self):
        """return a dataflow containing all records in storage.
        """
        return self.rec_m.getAll()

    def recordsInDaterange(self, bdate, edate):
        """return a dataflow containing specific records that specified
        by date range in storage.
        """
        return self.rec_m.date_range(bdate, edate)

    def figureOutRecords(self, bdate, edate, parsers = [], allrec=False):
        """
        """
        if allrec:
            data = self.allRecords()
        else:
            data = self.rec_m.date_range(bdate, edate)
        parser = RP.MainParser(data)
        parser.extend(parsers)
        return parser.parse()
    
    def saveProjects(self):
        savebuf = {}
        for name, proj in self.projects.items():
            savebuf[name] = proj.export_to_dict()
            savebuf[name]['projtype'] = proj.__class__.__name__
        Config.setProjectBuffer(savebuf)

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
        self.rec_m.clear()
        for key in self.projects:
            del self.projects[key]
        Config.setProjectBuffer(dict())

    def _setUpProjects(self):
        projbuf = Config.getProjectBuffer()
        if projbuf:
            # projbuf is not a empty dict
            for name, dictbuf in projbuf.items():
                projtype = dictbuf['projtype']
                proj = Projects.__dict__[projtype]()
                proj.import_from_dict(dictbuf)
                self.projects[name] = proj

    def _setUpRecords(self):
        recbuf = Config.getRecordBuffer()
        if recbuf:
            # recbuf is not a empty list
            for buf in recbuf:
                rdate, rec = buf2record(buf)
                self.addRecord(rdate, rec)
        # set record buffer up to default value a empty list.
        Config.setRecordBuffer(list())

    def _checkProjects(self, rdate, baserec, newrec=None, act='add'):
        if not self.projects:
            # there is no project in self.projects
            return
        
        for proj in self.projects.values():
            if proj.p_type == 'statistic':
                proj.register(rdate, baserec, newrec, act)
