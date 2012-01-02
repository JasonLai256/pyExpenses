#! /usr/bin/env python
# -*- coding:utf-8 -*-

import time
import sys
import os
import hashlib
try:
    import cPickle as Pickle
except:
    import Pickle
from datetime import date, timedelta
from decimal import Decimal
from collections import deque

import ErrorHandle as EH

class PwdError(Exception):
    pass

class BaseRecord(object):
    """Basic structure of single item use to store record.
    """
    def __init__(self, Type, Amount, Paidwith = '0',
                       Tag = '0', Note = None):
        self.csm_type = str(Type)    # ConsumingType
        self.amount = float(Amount)
        self.pmt_type = str(Paidwith)    # PaymentType
        self.csm_catag = str(Tag)
        self.comment = str(Note)

    def __eq__(self, brec):
        return self.csm_type == brec.csm_type and \
               self.amount == brec.amount and \
               self.pmt_type == brec.pmt_type and \
               self.csm_catag == brec.csm_catag and \
               self.comment == brec.comment

    def __ne__(self, brec):
        return not self == brec

    def getAttr(self, AttrType):
        if AttrType == "ConsumingType":
            return self.csm_type
        elif AttrType == "PaymentType":
            return self.pmt_type
        elif AttrType == "ConsumingCatagory":
            return self.csm_catag
        else:
            raise ValueError

    def copy(self, newrec):
        self.csm_type = newrec.csm_type
        self.amount = newrec.amount
        self.pmt_type = newrec.pmt_type
        self.csm_catag = newrec.csm_catag
        self.comment = newrec.comment

        
class _RecContainer(object):
    """Data container class inner defined."""
    def __init__(self, time):
        self._date = time
        self._storage = deque()

    def addContent(self, base_rec):
        self._storage.append(base_rec)

    def delElem(self, base_rec):
        """delete the specified element."""
        for elem in self._storage:
            if elem == base_rec:
                self._storage.remove(elem)
                return
            else:
                EH.valueError('data is not in Record Manipulator.')

    def updateElem(self, base_rec, new_rec):
        """update the specified element whth new_rec."""
        for elem in self._storage:
            if elem == base_rec:
                elem.copy(new_rec)
                return
            else:
                EH.valueError('data is not in Record Manipulator.')

class PickleImpl(object):
    """Record manipulator that offer some basic operations to mapulate data,
    like access,modify,retrieve etc.

    @Note: The format of seq -- data structure -- of PickleImpl class:

    _reclist[conta1, conta2, conta3, ... , contaN]  # list
             --+---
               |
               +--> _RecContainer(date, storage)  # class
                                        ---+---
                                           |
                  +------------------------+
                  |
                  +--> _storage[baserec1, baserec2, ... , baserecN]  # deque
                                ---+----
                                   |
                      +------------+
                      |
                      +--> BaseRecord(att1, att2, ... , attN)  # class

    """
    
    
    def __init__(self, pwd='<!--#/**/;;//PyExpense-->'):
        self._load(pwd)
        
        # following attributes is the info of records:
        self.sum_amounts = 0.0
        self.sum_items = 0
        
        self.max_item = 0    
        self.max_item_date = ''    # 最多记录项的一天
        
        self.max_amount = 0.0
        self.max_amount_date = ''

#    def __del__(self):
#        self._dump()

    def addItem(self, time, base_rec):
        """add a basic record to storage."""
        if not self.isExistence(time):
            item = _RecContainer(time)
            index = self._index(time)
            self._reclist.insert(index, item)
            self._len += 1

        self._updateStatus_add(base_rec)
        self._insert(time, base_rec)

    def delItem(self, date, base_rec):
        """delete a specified record.
        @note: if date not exist,raise a exception.
        """
        if not self.isExistence(date):
            EH.valueError('{0} is not in Record Manipulator.'.format(date))
        
        index = self._index(date)
        self._reclist[index].delElem(base_rec)

        if not len(self._reclist[index]._storage):
            # the element of _reclist has not BaseRecord
            del self._reclist[index]

    def updateItem(self, date, base_rec, new_rec):
        if not self.isExistence(date):
            EH.valueError('{0} is not in Record Manipulator.'.format(date))

        index = self._index(date)
        self._reclist[index].updateElem(base_rec, new_rec)

    def getAll(self):
        begin_d = self._reclist[0]._date
        end_d = self._reclist[-1]._date
        return self.record_range(begin_d, end_d)

    def getInfo(self):
        pass

    def date_range(self, begin, end):
        """Return a range of records in specified period.
        @note: 
        """
        if begin > end:
            EH.indexError(
                'Begin time {0} greater than end time {1}'.format(begin, end)
            )
        bindex = self._index(begin)
        eindex = self._index(end)

        ret = {}
        for elem in self._reclist[bindex:eindex]:
            ret[elem._date] = elem._storage
        return ret

    def clear(self):
        """clear all the data in data manipulator."""
        for elem in self._reclist[:]:
            for ite in xrange(len(elem._storage)):
                del elem._storage[0]
            del elem._date
            
        for ite in xrange(len(self._reclist)):
            del self._reclist[0]
        self._len = 0

    def save(self):
        self._dump()
        
    def importRecord(self, filename):
        """import a backup from specify file, note that it will override
        original data."""
        self.clear()  # NOTE: maybe should make this operation decide in upper level.
        file = open(filename)
        for line in file.readlines():
            dat = line.split(':')
            y = int(dat[0][:4])
            m = int(dat[0][5:7])
            d = int(dat[0][8:])
            rdate = date(y, m, d)
            tem = BaseRecord(dat[1], dat[2], dat[3], dat[4], dat[5])
            self.addItem(rdate, tem)
        else:
            file.close()

    def exportRecord(self, filename):
        """Export textual data records into the specified file.
        """
        file = open(filename, 'w')
        outlist = []
        for elem in self._reclist:
            outstr = ''
            for item in elem._storage:
                outstr += elem._date.isoformat()
                tem = ':' + item.csm_type + \
                    ':' + str(item.amount) + \
                    ':' + item.pmt_type + \
                    ':' + item.csm_catag + \
                    ':' + item.comment
                outstr += tem
            else:
                outlist.append(outstr)
        else:
            file.writelines(outlist)
            file.close()

    def _dump(self):
        fpath = os.path.join(os.path.abspath('.'), 'records.dat')
        picfile = open(fpath, 'wb')
        Pickle.dump(self._reclist, picfile, 2)
        Pickle.dump(self._pwd, picfile, 2)
        Pickle.dump(self._len, picfile, 2)
        picfile.close()

    def _load(self, pwd):
        fpath = os.path.join(os.path.abspath('.'), 'records.dat')
        isfile = os.path.isfile(fpath)
        if not isfile or not os.path.getsize(fpath):
            self._reclist = []
            m = hashlib.sha256()
            # There is a default common pwd digest.
            m.update('<!--#/**/;;//PyExpense-->')
            self._pwd = m.digest()
            self._len = 0
            if not isfile:
                # need to create a new store file of data
                self._dump()
        else:
            picfile = open(fpath)
            self._reclist = Pickle.load(picfile)
            self._pwd = Pickle.load(picfile)
            self._len = Pickle.load(picfile)
            picfile.close()
        
        m = hashlib.sha256()
        m.update(pwd)
        if m.digest() != self._pwd:
            raise PwdError

    def isExistence(self, dateitem):
        """Judge whether the item exist or not."""
        low = 0
        high = self._len - 1
        while True:
            if low > high:
                return False
            mid = (low + high) / 2
            try:            
                if self._reclist[mid]._date < dateitem:
                    low = mid + 1
                elif self._reclist[mid]._date == dateitem:
                    return True
                elif self._reclist[mid]._date > dateitem:
                    high = mid - 1
            except IndexError:
                print 'len = ', self._len, len(self._reclist)
                print 'low, mid, high = ', low, mid, high
                sys.exit(1)

    def _index(self, date):
        low = 0
        high = self._len - 1
        while True:
            # if can't find element then return the most matching position
            if low > high:
                return low
            mid = (low + high) / 2
            
            if self._reclist[mid]._date < date:
                low = mid + 1
            elif self._reclist[mid]._date == date:
                return mid
            elif self._reclist[mid]._date > date:
                high = mid - 1

    def _updateStatus_add(self, baserec):
        self.sum_amounts += baserec.amount
        self.sum_items += 1

    def _updateStatus_del(self, baserec):
        self.sum_amounts -= baserec.amount
        self.sum_items -= 1

    def _updateStatus_upd(self, baserec, newrec):
        self.sum_items += (baserec.amount - newrec.amount)
                
    def _insert(self, date, record):
        i = self._index(date)
        self._reclist[i].addContent(record)
