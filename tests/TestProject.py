#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys
import os
from datetime import date

from pyExpenses.Projects import *
from pyExpenses.Expense import Expense
from TestRecManip import TEST_SAMPS
from TestExpense import addSampleRecords


class TestConsumingProject(unittest.TestCase):

    def test_import_export_dict(self):
        proj = ConsumingProject(999, date(2012, 1, 1), 3333)
        
        dates = date(2012, 1, 1), date(2012, 1, 3)
        for d in dates:
            for rec in TEST_SAMPS[d]:
                proj.register(d, rec)

        tdict = proj.export_to_dict()
        proj2 = ConsumingProject()
        proj2.import_from_dict(tdict)

        self.assertEqual(proj.p_start_time, proj2.p_start_time)
        self.assertEqual(proj.p_accumt_amount, proj2.p_accumt_amount)
        self.assertEqual(proj.p_recs_amount, proj2.p_recs_amount)
        self.assertListEqual(proj.p_progress_info, proj2.p_progress_info)

        self.assertEqual(proj.p_accumt_amount, 103.0)
        self.assertEqual(proj.p_recs_amount, 4)

        tdict2 = proj2.export_to_dict()
        self.assertDictEqual(tdict, tdict2)

    def test_report(self):
        pass

    def test_register(self):
        expense = Expense()
        expense.setUp({'test':True})

        proj1 = ConsumingProject(9999, date(2012, 1, 1), 3333)
        proj2 = ConsumingProject(256, date(2012, 1, 1), 3333)
        proj3 = ConsumingProject(
            999, date(2012, 1, 1), 3333, 'type', u'Food & Drinks'
        )
        proj4 = ConsumingProject(
            300, date(2012, 1, 1), 3333, 'tag', u'Like'
        )
        expense.addProject('proj1', proj1)
        expense.addProject('proj2', proj2)
        expense.addProject('proj3', proj3)
        expense.addProject('proj4', proj4)
        addSampleRecords(expense)

        # test proj1
        self.assertEqual(proj1.p_accumt_amount, 2320.0)
        self.assertEqual(proj1.p_recs_amount, 21)
        self.assertEqual(proj1.p_accomplish_date, '')
        self.assertFalse(proj1.p_statdict['hasQuarter'])
        self.assertFalse(proj1.p_statdict['hasHalf'])
        self.assertFalse(proj1.p_statdict['hasThreeQuarters'])
        self.assertEqual(len(proj1.p_progress_info), 6)

        # test proj2
        self.assertEqual(proj2.p_accumt_amount, 2320.0)
        self.assertEqual(proj2.p_recs_amount, 21)
        self.assertEqual(proj2.p_accomplish_date, date.today().isoformat())
        self.assertTrue(proj2.p_statdict['hasQuarter'])
        self.assertTrue(proj2.p_statdict['hasHalf'])
        self.assertTrue(proj2.p_statdict['hasThreeQuarters'])
        self.assertEqual(
            proj2.p_statdict['DateOfQuarter'], date.today().isoformat()
        )
        self.assertEqual(
            proj2.p_statdict['DateOfHalf'], date.today().isoformat()
        )
        self.assertEqual(
            proj2.p_statdict['DateOfThreeQuarters'], date.today().isoformat()
        )
        self.assertEqual(len(proj2.p_progress_info), 7)

        # test proj3
        self.assertEqual(proj3.p_accumt_amount, 322.0)
        self.assertEqual(proj3.p_recs_amount, 16)
        self.assertEqual(proj3.p_accomplish_date, '')
        self.assertTrue(proj3.p_statdict['hasQuarter'])
        self.assertFalse(proj3.p_statdict['hasHalf'])
        self.assertFalse(proj3.p_statdict['hasThreeQuarters'])
        self.assertEqual(
            proj3.p_statdict['DateOfQuarter'], date.today().isoformat()
        )
        self.assertEqual(len(proj3.p_progress_info), 7)

        # test proj4
        self.assertEqual(proj4.p_accumt_amount, 154.0)
        self.assertEqual(proj4.p_recs_amount, 2)
        self.assertEqual(proj4.p_accomplish_date, '')
        self.assertTrue(proj4.p_statdict['hasQuarter'])
        self.assertTrue(proj4.p_statdict['hasHalf'])
        self.assertFalse(proj4.p_statdict['hasThreeQuarters'])
        self.assertEqual(
            proj4.p_statdict['DateOfQuarter'], date.today().isoformat()
        )
        self.assertEqual(
            proj4.p_statdict['DateOfHalf'], date.today().isoformat()
        )
        self.assertEqual(len(proj4.p_progress_info), 7)
