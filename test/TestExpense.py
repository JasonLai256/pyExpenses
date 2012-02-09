#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys
import os
from datetime import date

try:
    from pyExpenses.Expense import Expense
except ImportError:
    sys.path.append(os.path.abspath('..'))
    from pyExpenses.Expense import Expense
from pyExpenses import Projects
from pyExpenses.ConfigManip import Config
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
        

    def test_figureOutRecords(self):
        pass

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


if __name__ == '__main__':
    unittest.main()
