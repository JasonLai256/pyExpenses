#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
    pyExpenses.Record
    ~~~~~~~~~~~~~~~~~

    Implements the unit object of expense's record for pyExpenses.

    :copyright: (c) 2012 by Jason Lai.
    :license: BSD, see LICENSE for more details.
"""


class BaseRecord(object):
    """Basic structure of single item use to store record.
    """
    def __init__(self, Amount, Type, Payment, Currency, Tag='', Note=''):
        self.amount = float(Amount)
        # Note: type structure is a 2-tuple, e.g, (type, subtype)
        self.type = unicode(Type[0].encode('utf-8'), 'utf-8'), \
                    unicode(Type[1].encode('utf-8'), 'utf-8')
        self.payment = unicode(Payment.encode('utf-8'), 'utf-8')
        self.currency = unicode(Currency.encode('utf-8'), 'utf-8')
        self.tag = unicode(Tag.encode('utf-8'), 'utf-8')
        self.comment = unicode(Note.encode('utf-8'), 'utf-8')

    def __eq__(self, brec):
        return self.type == brec.type and \
               self.amount == brec.amount and \
               self.payment == brec.payment and \
               self.currency == brec.currency and \
               self.tag == brec.tag and \
               self.comment == brec.comment

    def __ne__(self, brec):
        return not self == brec

    def copy(self, nrec):
        self.type = nrec.type
        self.amount = nrec.amount
        self.payment = nrec.payment
        self.currency = nrec.currency
        self.tag = nrec.tag
        self.comment = nrec.comment
