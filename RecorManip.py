#! /usr/bin/env python
# -*- coding:utf-8 -*-

import time
import sys
import os
from datetime import date
from decimal import Decimal
from collections import deque
import ErrorHandle as EH

class BaseRecord(object):
    """保存记录的基本结构体，仅仅是条项记录功能
    """
    def __init__(self, Type, Amount, Paidwith = '0',
                       Tag = '0', Note = None):
        self.csm_type = str(Type)    # ConsumingType
        self.amount = float(Amount)
        self.pmt_type = str(Paidwith)    # PaymentType
        self.csm_catag = str(Tag)
        self.comment = str(Note)

    def __eq__(self, brec):
        """判断传入参数是否与当前instance的属性相同 (==)."""
        return self.csm_type == brec.csm_type and \
               self.amount == brec.amount and \
               self.pmt_type == brec.pmt_type and \
               self.csm_catag == brec.csm_catag and \
               self.comment == brec.comment

    def __ne__(self, brec):
        """判断传入参数是否与当前instance的属性不同 (!=)."""
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


class RecorManip(object):
    """数据管理器，负责最基本的access,modify,retrieve等功能
    """
    # testing control notation
    _test = False
    
    def __init__(self):
        self._reclist = []
        # Note: _len is the amount of elements in _reclist.
        self._len = 0

        # following attributes is the info of records:
        self.sum_amounts = 0.0
        self.sum_items = 0
        
        self.max_item = 0    
        self.max_item_date = ''    # 最多记录项的一天
        
        self.max_amount = 0.0
        self.max_amount_date = ''

    def addItem(self, time, base_rec):
        """添加一项纪录。"""
        if RecorManip._test:
            print "\tfunction: addItem"
        if not self.isExistence(time):
            item = _RecContainer(time)
            index = self._index(time)
            self._reclist.insert(index, item)
            self._len += 1

        self._updateStatus_add(base_rec)
        self._insert(time, base_rec)

    def delItem(self, date, base_rec):
        """delete one specified record.
        @note: if date not exist,raise a exception.
        """
        if RecorManip._test:
            print "\tfunction: delItem"
        if not self.isExistence(date):
            EH.valueError('{0} is not in Record Manipulator.'.format(date))
        
        index = self._index(date)
        self._reclist[index].delElem(base_rec)

        if not len(self._reclist[index]._storage):
            # the element of _reclist has not BaseRecord
            del self._reclist[index]

    def updateItem(self, date, base_rec, new_rec):
        if RecorManip._test:
            print "\tfunction: updateItem"
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

    def record_range(self, begin, end):
        """Return a range of records in specified period.
        @note: 
        """
        if RecorManip._test:
            print "\tfunction: record_range"
        if begin > end:
            EH.indexError(
                'Begin time greater {0} than end time {1}'.format(begin, end)
            )
        begin_ind = self._index(begin)
        end_ind = self._index(end) + 1
        ret = deque()
        for elem in self._reclist[begin_ind:end_ind]:
            ret.append( (elem._date, elem._storage) )
        return ret

    def findDate(self, date):
        """find and return the matching record. 
        @note: if date not exist,raise a exception.
        """
        if RecorManip._test:
            print "\tfunction: findDate"
        if not self.isExistence(date):
            EH.valueError('{0} is not in Record Manipulator.'.format(date))
        
        index = self._index(date)
#        print 'index = ', index
        return date, self._reclist[index]._storage
        
    def findDates(self, date, nth):
        """ """
        if RecorManip._test:
            print "\tfunction: findDates"
        index = self._index(date)
        ret = deque()
        for elem in self._reclist[index:index + nth]:
            ret.append( (elem._date, elem._storage) )
        return ret

    def clear(self):
        """clear all the data in data manipulator."""
        if RecorManip._test:
            print "\tfunction: clear"
        for elem in self._reclist[:]:
            for ite in xrange(len(elem._storage)):
                del elem._storage[0]
            del elem._date
            
        for ite in xrange(len(self._reclist)):
            del self._reclist[0]
        self._len = 0

    def importRecord(self, filename):
        """备份数据到指定文件"""
        if RecorManip._test:
            print "\tfunction: importRecord"
        self.clear()
        file = open(filename)
        for line in file.readlines():
            dat = line.split(':')
            tem = BaseRecord(dat[1], dat[2], dat[3], dat[4], dat[5])
            self.addItem(dat[0], tem)
        else:
            file.close()

    def exportRecord(self, filename):
        """Export data records into the specified file.
        """
        if RecorManip._test:
            print "\tfunction: exportRecord"
        file = open(filename, 'w')
        outlist = []
        for elem in self._reclist:
            outstr = ''
            for item in elem._storage:
                outstr += elem._date
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

    def isExistence(self, dateitem):
        """Judge whether the item exist or not."""
        if RecorManip._test:
            print "\tfunction: isExistence"
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
        if RecorManip._test:
            print "\tfunction: _index"
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
        if RecorManip._test:
            print "\tfunction: _insert"
        i = self._index(date)
        self._reclist[i].addContent(record)

    def test(self):
        for item in self._reclist:
            print item._date, '\tlenght is ', len(item._storage)
        print 'lenght = ', self._len




if __name__ == '__main__':
    starttime = time.time()
    
    rm = RecorManip()
    rm.importRecord('/home/jason/Py/Expenses/example.dat')
    
    print '\n', '=' * 40, '\n'
    print rm.isExistence('2011-01-01')
    print rm.isExistence('2011-05-01')
    dat = rm.findDates('2011-04-11', 100)
    for k, v in dat:
        print k, ' : ', len(v)


    print '\n', 30 * '-', '\n'
    dat2 = rm.record_range('2011-01-01', '2011-07-04')
    for k, v in dat2:
        print k, ' : ', len(v)
        
    print '\n', 30 * '-', '\n'    
    dat3 = rm.findDate('2011-06-18')
    for elem in dat3[1]:
        print dat3[0], elem.csm_type, elem.amount

        
    print '\n', 30 * '-', '\n'
    tem = BaseRecord(6, 62.958968721, 2, 1)
#    newbr  = BaseRecord(5, 31)
#    rm.updateItem('2006-05-18', tem, newbr)
#    rm.delItem('2006-05-18', newbr)
    tem = BaseRecord('0', 1)
    newbr  = BaseRecord('1', '3131.33')
#    rm.updateItem('2011-06-18', tem, newbr)
    
    dat = rm.findDate('2011-06-18')
    for elem in dat[1]:
        print dat[0], elem.csm_type, elem.amount


    print '\n', 30 * '-', '\n'
    tem = BaseRecord('4', 3)
    rm.addItem('2011-05-01', tem)
    dat2 = rm.record_range('2011-01-01', '2011-07-04')
    for k, v in dat2:
        print k, ' : ', len(v)


    print '\n', 30 * '-', '\n'
#    rm.test()
    rm.exportRecord('/home/jason/Py/Expenses/example_export.dat')
    print "Amount Sum = {0}, Items Sum = {1}\n" \
        "Max Item Date = {2}, Max Items = {3}\n" \
        "Max Amount Date = {4}, Max Amount = {5}".format(rm.sum_amounts,
                                                         rm.sum_items,
                                                         rm.max_item_date,
                                                         rm.max_item,
                                                         rm.max_amount_date,
                                                         rm.max_amount)
    rm.clear()
    print '\n', 30 * '-', '\n'
#    rm.test()


    print '\n', 30 * '-', '\n'
    rm2 = RecorManip()
    rm2.importRecord('/home/jason/Py/Expenses/example_export.dat')
    
    print '\n', '=' * 40, '\n'
    print rm.isExistence('2011-01-01')
    print rm.isExistence('2011-05-01')
    dat = rm.findDates('2011-04-11', 100)
    for k, v in dat:
        print k, ' : ', len(v)
    rm.clear()
    
    tem = BaseRecord('4', 3)
    rm.addItem('2008-05-01', tem)
    tem = BaseRecord('4', 3)
    rm.addItem('2009-05-01', tem)
    tem = BaseRecord('4', 3)
    rm.addItem('2010-05-01', tem)
    tem = BaseRecord('4', 3)
    rm.addItem('2012-05-01', tem)
    tem = BaseRecord('4', 3)
    rm.addItem('2013-05-01', tem)
    rm.exportRecord('/home/jason/Py/Expenses/example_export2.dat')
    
    

    print '调用过程用时为：{0:.3f}s'.format(time.time() - starttime)
