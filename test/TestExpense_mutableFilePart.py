#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys
import os
from datetime import date

from pyExpenses.Expense import Expense
from TestExpense import addSampleRecords
from pyExpenses.RecManipImpl import DEFAULT_PASSWORD


class TestExpense_mutableFilePart(unittest.TestCase):
    """WARNING: Note that this test will replace the record.db file in 
    package derectory, there is nonrevertible, be careful use this test.
    """

    def test_Expense_mutable_operation(self):
        expense = Expense()
        expense.setUp()
        addSampleRecords(expense)

        expense.updatePassword(DEFAULT_PASSWORD, 'JL')
        expense.save()

        exp2 = Expense()
        exp2.setUp({'pwd':'JL'})
        self.assertEqual(
            sum(len(cont._storage) for cont in expense.rec_m.impl._reclist),
            sum(len(cont._storage) for cont in exp2.rec_m.impl._reclist),
        )
        self.assertEqual(
            expense.rec_m.impl._pwd,
            exp2.rec_m.impl._pwd,
        )
        self.assertEqual(
            expense.rec_m.impl._len,
            exp2.rec_m.impl._len,
        )

        exp2.resetAll()
