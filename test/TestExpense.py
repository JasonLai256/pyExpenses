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


class TestExpense(unittest.TestCase):

    def setUp(self):
        self.expense = Expense()

    def test_addRecord(self):
        pass

    def test_deleteRecord(self):
        pass

    def test_updeteRecord(self):
        pass

    # def test_(self):
    #     pass

    # def test_(self):
    #     pass



if __name__ == '__main__':
    unittest.main()
