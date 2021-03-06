#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys
import os
from datetime import date

from pyExpenses.Expense import Expense
from pyExpenses import Projects
from pyExpenses.ConfigManip import Config
import pyExpenses.RecParser as RP
from pyExpenses.Record import BaseRecord
from TestRecManip import TEST_SAMPS


def addSampleRecords(exp):
    for rdate, recs in TEST_SAMPS.items():
        for rec in recs:
            exp.addRecord(rdate, rec)

class TestExpense(unittest.TestCase):

    def setUp(self):
        self.expense = Expense()

    def test_addRecord(self):
        addSampleRecords(self.expense)
        
        recbuf = Config.getRecordBuffer()
        self.assertEqual(
            len(recbuf), 21
        )
        self.expense.setUp({'test':True})
        
        recbuf = Config.getRecordBuffer()
        self.assertEqual(
            len(recbuf), 0
        )

    def test_deleteRecord(self):
        with self.assertRaises(AttributeError):
            self.expense.deleteRecord(
                date(2012, 1, 1),
                TEST_SAMPS[date(2012, 1, 1)][0]
            )

        self.expense.setUp({'test':True})
        addSampleRecords(self.expense)
        
        self.expense.deleteRecord(
            date(2012, 1, 1),
            TEST_SAMPS[date(2012, 1, 1)][0]
        )

    def test_updeteRecord(self):
        with self.assertRaises(AttributeError):
            self.expense.updateRecord(
                date(2012, 1, 1),
                TEST_SAMPS[date(2012, 1, 1)][0],
                TEST_SAMPS[date(2012, 1, 1)][1]
            )

        self.expense.setUp({'test':True})
        addSampleRecords(self.expense)
        
        self.expense.updateRecord(
            date(2012, 1, 1),
            TEST_SAMPS[date(2012, 1, 1)][0],
            BaseRecord(15, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY')
        )

    def test_add_delete_and_list_project(self):
        self.expense.setUp({'test':True})

        class test:
            pass

        proj1 = Projects.ConsumingProject()
        proj2 = Projects.ConsumingProject()
        proj3 = test()
        proj4 = test()
        proj5 = test()
        proj6 = test()
        proj3.p_type = proj4.p_type = proj5.p_type = proj6.p_type = 'other'

        self.expense.addProject('proj1', proj1)
        self.expense.addProject('proj2', proj2)
        self.expense.addProject('proj3', proj3)
        self.expense.addProject('proj4', proj4)
        self.expense.addProject('proj5', proj5)
        self.expense.addProject('proj6', proj6)

        self.assertEqual(
            len(list(self.expense.listProject())), 6
        )
        self.assertEqual(
            len(list(self.expense.listProject(ptype='statistic'))), 2
        )
        self.assertEqual(
            len(list(self.expense.listProject(ptype='other'))), 4
        )
        for name, proj in self.expense.listProject():
            self.assertTrue(name.startswith('proj'))
            if proj.p_type == 'statistic':
                self.assertIsNotNone(
                    proj.export_to_dict()
                )

        self.expense.deleteProject('proj1')
        self.expense.deleteProject('proj5')
        self.assertEqual(
            len(list(self.expense.listProject())), 4
        )
        self.assertEqual(
            len(list(self.expense.listProject(ptype='statistic'))), 1
        )
        self.assertEqual(
            len(list(self.expense.listProject(ptype='other'))), 3
        )

    def test_save_and_setUp_Projects(self):
        self.expense.setUp({'test':True})

        proj1 = Projects.ConsumingProject(9999, date(2012, 1, 1), 3333)
        proj2 = Projects.ConsumingProject(
            999, date(2012, 1, 1), 3333, 'type', u'Food & Drinks'
        )
        self.expense.addProject('proj1', proj1)
        self.expense.addProject('proj2', proj2)
        addSampleRecords(self.expense)

        self.expense.saveProjects()
        expense2 = Expense()
        expense2.setUp({'test':True})

        self.assertEqual(len(expense2.projects), 2)
        self.assertDictEqual(
            expense2.projects['proj1'].export_to_dict(),
            self.expense.projects['proj1'].export_to_dict()
        )
        self.assertDictEqual(
            expense2.projects['proj2'].export_to_dict(),
            self.expense.projects['proj2'].export_to_dict()
        )

        Config.setProjectBuffer(dict())

    def test_getRecords(self):
        self.expense.setUp({'test':True})
        addSampleRecords(self.expense)

        bdate = date(2012, 1, 2)
        edate = date(2012, 1, 9)
        recseq = self.expense.getRecords(bdate, edate)
        # test number of days
        self.assertEqual(len(recseq), 6)
        # test number of records
        self.assertEqual(
            sum(len(recseq[dat]) for dat in recseq),
            10
        )
        
    def test_parseByRecords(self):
        self.expense.setUp({'test':True})
        addSampleRecords(self.expense)

        allrecs = self.expense.allRecords()
        
        # test_General_Analys
        analyres, dummy1, dummy2 = self.expense.parseByRecords(allrecs)
        rdict = {}
        for key, amount, percent in analyres[0][1]:
            rdict[key] = amount
        self.assertEqual(
            rdict[u'Food & Drinks'], 322.0
        )
        self.assertEqual(
            rdict[u'Learning & Education'], 121.0
        )
        self.assertEqual(
            rdict[u'Digital devices'], 1798.0
        )
        self.assertEqual(
            rdict[u'Transport costs'], 16.0
        )
        self.assertEqual(
            rdict[u'Health care'], 13.0
        )
        self.assertEqual(
            rdict[u'Recreation'], 50.0
        )

        # test_MthsInYear_Filter
        dummy1, dummy2, fseq = self.expense.parseByRecords(allrecs, [RP.MthsInYear_Filter([1])])
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            2320.0
        )

        # test_Money_Filter
        dummy1, dummy2, fseq = self.expense.parseByRecords(allrecs, [RP.Money_Filter(20)])
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            161.0
        )

        # test_Type_Filter
        dummy1, dummy2, fseq = self.expense.parseByRecords(allrecs, [RP.Type_Filter((u'Food & Drinks', u'Meal'), 'type')])
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            227.0
        )

    def test_parseByDateRange(self):
        self.expense.setUp({'test':True})
        addSampleRecords(self.expense)

        bdate = date(2012, 1, 1)
        edate = date(2012, 2, 9)
        # test_General_Analys
        analyres, dummy1, dummy2 = self.expense.parseByDateRange(bdate, edate)
        rdict = {}
        for key, amount, percent in analyres[0][1]:
            rdict[key] = amount
        self.assertEqual(
            rdict[u'Food & Drinks'], 322.0
        )
        self.assertEqual(
            rdict[u'Learning & Education'], 121.0
        )
        self.assertEqual(
            rdict[u'Digital devices'], 1798.0
        )
        self.assertEqual(
            rdict[u'Transport costs'], 16.0
        )
        self.assertEqual(
            rdict[u'Health care'], 13.0
        )
        self.assertEqual(
            rdict[u'Recreation'], 50.0
        )

        # test_MthsInYear_Filter
        dummy1, dummy2, fseq = self.expense.parseByDateRange(bdate, edate, [RP.MthsInYear_Filter([1])])
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            2320.0
        )

        # test_Money_Filter
        dummy1, dummy2, fseq = self.expense.parseByDateRange(bdate, edate, [RP.Money_Filter(20)])
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            161.0
        )

        # test_Type_Filter
        dummy1, dummy2, fseq = self.expense.parseByDateRange(bdate, edate, [RP.Type_Filter((u'Food & Drinks', u'Meal'), 'type')])
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            227.0
        )

    def test_buf2record_and_record2buf(self):
        from pyExpenses.utils import buf2record, record2buf
        rdate = date(2012, 1, 7)
        rec = TEST_SAMPS[rdate][0]
        buf = record2buf(rdate, rec)
        temdate, temrec = buf2record(buf)

        self.assertEqual(
            rdate.isoformat(), temdate.isoformat()
        )
        self.assertEqual(rec.amount, temrec.amount)
        self.assertEqual(rec.type, temrec.type)
        self.assertEqual(rec.payment, temrec.payment)
        self.assertEqual(rec.currency, temrec.currency)
        self.assertEqual(rec.tag, temrec.tag)
        self.assertEqual(rec.comment, temrec.comment)
