#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys
import os
from datetime import date

try:
    import pyExpenses.RecParser as RP
except ImportError:
    sys.path.append(os.path.abspath('..'))
    import pyExpenses.RecParser as RP
from pyExpenses.RecManipImpl import BaseRecord
from pyExpenses.RecManip import RecManip
from TestRecManip import TEST_SAMPS


class TestRecParser(unittest.TestCase):

    def setUp(self):
        self.rmanip = RecManip(test=True)
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
        parser.append(RP.Type_Filter((u'食品酒水', u'早午晚餐'), 'type'))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            227.0
        )

        parser = RP.MainParser(self.dataflow)
        parser.append(RP.Type_Filter(u'学习进修', 'type'))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            1919.0
        )

        parser = RP.MainParser(self.dataflow)
        parser.append(RP.Type_Filter(u'信用卡', 'payment'))
        dummy1, dummy2, fseq = parser.parse()
        self.assertEqual(
            sum(rec.amount for rdate in fseq
                               for rec in fseq[rdate]),
            1969.0
        )

        parser = RP.MainParser(self.dataflow)
        parser.append(RP.Type_Filter(u'赞', 'tag'))
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
            rdict[u'食品酒水'], 322.0
        )
        self.assertEqual(
            rdict[u'学习进修'], 1919.0
        )
        self.assertEqual(
            rdict[u'行车交通'], 16.0
        )
        self.assertEqual(
            rdict[u'医疗保健'], 13.0
        )
        self.assertEqual(
            rdict[u'休闲娱乐'], 50.0
        )

        
if __name__ == '__main__':
    unittest.main()

