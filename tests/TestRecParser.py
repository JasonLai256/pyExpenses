#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys
import os
from datetime import date

import pyExpenses.RecParser as RP
from pyExpenses.Record import BaseRecord
from pyExpenses.RecManip import RecManip
from TestRecManip import TEST_SAMPS


class TestRecParser(unittest.TestCase):

    def setUp(self):
        self.rmanip = RecManip()
        self.rmanip.setUp(test=True)
        for rdate, recs in TEST_SAMPS.items():
            for rec in recs:
                self.rmanip.addItem(rdate, rec)
        self.dataflow = self.rmanip.getAll()

    # analy, stst, filter
    def test_Amount_Stat(self):
        parser = RP.MainParser(self.dataflow)
        parser.append(RP.Amount_Stat())
        dummy1, statres, dummy2 = parser.parse()
        self.assertEqual(statres[0][1], 2320.0)

    def test_Count_Stat(self):
        parser = RP.MainParser(self.dataflow)
        parser.append(RP.Count_Stat())
        dummy1, statres, dummy2 = parser.parse()
        self.assertEqual(statres[0][1], 21)

    def test_Type_Filter(self):
        parser = RP.MainParser(self.dataflow)
        parser.append(RP.Type_Filter((u'Food & Drinks', u'Meal'), 'type'))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            227.0
        )

        parser = RP.MainParser(self.dataflow)
        parser.append(RP.Type_Filter(u'Digital devices', 'type'))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            1798.0
        )

        parser = RP.MainParser(self.dataflow)
        parser.append(RP.Type_Filter(u'Credit card', 'payment'))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            1969.0
        )

        parser = RP.MainParser(self.dataflow)
        parser.append(RP.Type_Filter(u'Like', 'tag'))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            154.0
        )

    def test_Money_Filter(self):
        # TODO: modify Money_Filter range that is [start, stop)
        parser = RP.MainParser(self.dataflow)
        parser.append(RP.Money_Filter(20))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            161.0
        )
        
        parser = RP.MainParser(self.dataflow)
        parser.append(RP.Money_Filter(30, 100))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            134.0
        )

    def test_DaysInWeek_Filter(self):
        parser = RP.MainParser(self.dataflow)
        parser.append(RP.DaysInWeek_Filter([5, 6]))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            131.0
        )

    def test_DaysInMonth_Filter(self):
        parser = RP.MainParser(self.dataflow)
        parser.append(RP.DaysInMonth_Filter([2, 4, 6, 8, 10]))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            164.0
        )

    def test_MthsInYear_Filter(self):
        parser = RP.MainParser(self.dataflow)
        parser.append(RP.MthsInYear_Filter([1]))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            2320.0
        )

        parser = RP.MainParser(self.dataflow)
        parser.append(RP.MthsInYear_Filter([2]))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            0.0
        )

    def test_General_Analys(self):
        parser = RP.MainParser(self.dataflow)
        parser.append(RP.General_Analys())
        analyres, dummy1, dummy2 = parser.parse()

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
