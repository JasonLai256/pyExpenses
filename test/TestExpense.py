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
from TestRecManip import TEST_SAMPS


class TestExpense(unittest.TestCase):

    def setUp(self):
        self.expense = Expense()

    def test_addRecord(self):
        pass

    def test_deleteRecord(self):
        with self.assertRaises(AttributeError):
            self.expense.deleteRecord(
                date(2012, 1, 1),
                TEST_SAMPS[date(2012, 1, 1)][0]
            )

        self.expense.setUp({'test':True})
        
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

    # def test_(self):
    #     pass

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
