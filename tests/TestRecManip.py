#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys
import os
from datetime import date

from pyExpenses.RecManip import RecManip
from pyExpenses.Record import BaseRecord


TEST_SAMPS = {
    date(2012, 1, 1): [
        BaseRecord(21, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY'),
        BaseRecord(51, (u'Food & Drinks', u'Snacks'), u'Cash', u'CHY', u'', u'a little regret.')
    ],
    date(2012, 1, 2): [
        BaseRecord(18, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY')
    ],
    date(2012, 1, 3): [
        BaseRecord(18, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY'),
        BaseRecord(13, (u'Health care', u'Health spending'), u'Cash', u'CHY')
    ],
    date(2012, 1, 4): [
        BaseRecord(22, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY')
    ],
    date(2012, 1, 5): [
        BaseRecord(19, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY', ),
        BaseRecord(121, (u'Learning & Education', u'Books'), u'Credit card', u'CHY', u'Like'),
        BaseRecord(11, (u'Food & Drinks', u'Snacks'), u'Cash', u'CHY')
    ],
    date(2012, 1, 7): [
        BaseRecord(33, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY', u'Like', u'expensive but there is very nice experience.')
    ],
    date(2012, 1, 8): [
        BaseRecord(15, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY'),
        BaseRecord(11, (u'Food & Drinks', u'Snacks'), u'Cash', u'CHY')
    ],
    date(2012, 1, 9): [
        BaseRecord(20, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY')
    ],
    date(2012, 1, 10): [
        BaseRecord(18, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY'),
        BaseRecord(14, (u'Food & Drinks', u'Snacks'), u'Cash', u'CHY'),
        BaseRecord(16, (u'Transport costs', u'Public Transport'), u'Cash', u'CHY'),
        BaseRecord(50, (u'Recreation', u'Entertainment'), u'Credit card', u'CHY', u'', u'goto theater.')
    ],
    date(2012, 1, 12): [
        BaseRecord(23, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY'),
        BaseRecord(8, (u'Food & Drinks', u'Snacks'), u'Cash', u'CHY')
    ],
    date(2012, 1, 13): [
        BaseRecord(20, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY'),
        BaseRecord(1798, (u'Digital devices', u'Tablets'), u'Credit card', u'CHY', u'Expensive', u'buy a nook tablet from taobao.')
    ]
}


class TestRecManip(unittest.TestCase):

    def setUp(self):
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.rmanip = RecManip()
        self.rmanip.setUp(test=True)
        for rdate, recs in TEST_SAMPS.items():
            for rec in recs:
                self.rmanip.addItem(rdate, rec)

    def test_clear(self):
        res = self.rmanip.getAll()
        self.assertNotEqual(len(res), 0)
        
        self.rmanip.clear()
        res = self.rmanip.getAll()
        self.assertEqual(len(res), 0)

    def test_addItem(self):
        rdate = date(2011, 12, 28)
        brec = BaseRecord(28, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY')
        self.rmanip.addItem(rdate, brec)
        
        res = self.rmanip.findDate(rdate)
        self.assertEqual(len(res[rdate]), 1)
        self.assertEqual(
            sum(rec.amount for rec in res[rdate]),
            28.0
        )

    def test_delItem(self):
        rdate = date(2012, 1, 5)
        res = self.rmanip.findDate(rdate)
        # print 'length: ', len(res)
        self.assertEqual(len(res[rdate]), 3)

        brec = BaseRecord(11, (u'Food & Drinks', u'Snacks'), u'Cash', u'CHY')
        self.rmanip.delItem(rdate, brec)
        res = self.rmanip.findDate(rdate)
        self.assertEqual(len(res[rdate]), 2)

    def test_updateItem(self):
        rdate = date(2012, 1, 4)
        res = self.rmanip.findDate(rdate)
        upd_rec = res[rdate][0]
        self.assertEqual(upd_rec.amount, 22.0)

        new_rec = BaseRecord(33, (u'Food & Drinks', u'Meal'), u'Cash', u'CHY')
        self.rmanip.updateItem(rdate, upd_rec, new_rec)
        res = self.rmanip.findDate(rdate)
        self.assertEqual(res[rdate][0].amount, 33.0)

    def test_getAll(self):
        res = self.rmanip.getAll()
        self.assertEqual(len(res), 11)
        self.assertEqual(
            sum(rec.amount for rdate in res
                               for rec in res[rdate]),
            2320.0
        )

    def test_getInfo(self):
        # TODO: need to complete the implementation of RecManip.getInfo() priorly.
        pass

    def test_date_range(self):
        bdate = date(2012, 1, 1)
        edate = date(2012, 1, 7)
        res = self.rmanip.date_range(bdate, edate)
        self.assertEqual(len(res), 5)
        self.assertIsNone(res.get(edate, None))
        self.assertEqual(
            sum(rec.amount for rdate in res
                               for rec in res[rdate]),
            294.0
        )

    def test_findDate(self):
        rdate = date(2012, 1, 13)
        res = self.rmanip.findDate(rdate)
        self.assertEqual(len(res[rdate]), 2)
        self.assertEqual(
            sum(rec.amount for rec in res[rdate]),
            1818.0
        )

    def test_findDates(self):
        rdate = date(2012, 1, 8)
        res = self.rmanip.findDates(rdate, 5)
        self.assertEqual(len(res), 4)
        self.assertIsNone(
            res.get(date(2012, 1, 13), None)
        )
        self.assertEqual(
            sum(rec.amount for keydate in res
                               for rec in res[keydate]),
            175.0
        )
    
    def test_import_export_Record(self):
        fpath = os.path.join(self.path, 'temp_rec.csv')
        self.rmanip.exportRecord(fpath)
        new_rmanip = RecManip()
        new_rmanip.setUp(test=True)
        new_rmanip.importRecord(fpath)

        ores = self.rmanip.getAll()
        nres = new_rmanip.getAll()
        
        self.assertEqual(len(ores), len(nres))
        self.assertEqual(
            sum(rec.amount for keydate in ores
                               for rec in ores[keydate]),
            sum(rec.amount for keydate in nres
                               for rec in nres[keydate])
        )

