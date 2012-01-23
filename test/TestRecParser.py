#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys
import os
from datetime import date

try:
    from RecParser import RecParser as RP
except ImportError:
    sys.path.append(os.path.abspath('..'))
    from RecParser import RecParser as RP
from RecManipImpl import BaseRecord
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
        parser.append(RP.)

        # TODO: need to be done.

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
        # TODO: need to be modify that suit to the BaseRecord new features
        
        # self.assertEqual(analyres[0][1], 21)
        # self.assertEqual(analyres[0][1], 21)
        # self.assertEqual(analyres[0][1], 21)

        
if __name__ == '__main__':
    unittest.main()

