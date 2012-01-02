#! /usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import date, timedelta

from RecManipImpl import *
from ConfigManip import Config


class RecManip(object):
    def __init__(self):
        self.impl = PickleImpl()

    def addItem(self, time, base_rec):
        """add a basic record to storage."""
        self.impl.addItem(time, base_rec)

    def delItem(self, date, base_rec):
        """delete a specified record.
        @NOTE: if date not exist,raise a exception.
        """
        self.impl.delItem(date, base_rec)

    def updateItem(self, date, base_rec, new_rec):
        self.impl.updateItem(date, base_rec, new_rec)

    def getAll(self):
        return self.impl.getAll()

    def getInfo(self):
        return self.impl.getInfo()

    def date_range(self, begin, end):
        """Return a range of records in specified period.
        @NOTE:
        """
        return self.impl.date_range(begin, end)

    def findDate(self, fdate):
        """find and return the matching record. 
        @NOTE: if date not exist,raise a exception.
        """
        return self.impl.date_range(fdate, fdate + timedelta(1))

    def findDates(self, fdate, nth=0):
        return self.impl.date_range(fdate, fdate + timedelta(nth))

    def clear(self):
        """clear all the data in data manipulator."""
        self.impl.clear()

    def save(self):
        """save all the data in data manipulator to permanent storage."""
        self.impl.save()

    def importRecord(self, filename):
        self.impl.importRecord(filename)

    def exportRecord(self, filename):
        self.impl.exportRecord(filename)



if __name__ == '__main__':
    starttime = time.time()
    
    rm = RecManip()
    rm.importRecord('/home/jason/Py/Expenses/example.dat')
#    rm.save()
    
    print '\n', '=' * 40, '\n'
    print rm.impl.isExistence(date(2011, 1, 1))
    print rm.impl.isExistence(date(2011, 5, 1))
    dat = rm.findDates(date(2011, 4, 11), 100)
    for k in dat:
        print k, ' : ', len(dat[k])


    print '\n', 30 * '-', '\n'
    dat2 = rm.date_range(date(2011, 1, 1), date(2011, 7, 4))
    for k in dat2:
        print k, ' : ', len(dat2[k])
        
    print '\n', 30 * '-', '\n'    
    dat3 = rm.findDate(date(2011, 6, 18))
    for k, v in dat3.items():
        print k, '\n'
        for elem in v:
            print ' - ', elem.csm_type, ', ', elem.amount

        
    print '\n', 30 * '-', '\n'
    tem = BaseRecord(6, 62.958968721, 2, 1)
#    newbr  = BaseRecord(5, 31)
#    rm.updateItem(date(2006, 5, 18), tem, newbr)
#    rm.delItem(date(2006, 5, 18), newbr)
    tem = BaseRecord('0', 1)
    newbr  = BaseRecord('1', '3131.33')
#    rm.updateItem(date(2011, 6, 18), tem, newbr)
    
    dat = rm.findDate(date(2010, 6, 18))
    for k, v in dat.items():
        print k, '\n'
        for elem in v:
            print ' - ', elem.csm_type, ', ', elem.amount


    print '\n', 30 * '-', '\n'
    tem = BaseRecord('4', 3)
    rm.addItem(date(2011, 5, 1), tem)
    dat2 = rm.date_range(date(2011, 1, 1), date(2011, 7, 4))
    for k in dat2:
        print k, ' : ', len(dat2[k])


    print '\n', 30 * '-', '\n'
#    rm.test()
    rm.exportRecord('/home/jason/Py/Expenses/example_export.dat')
    print "Amount Sum = {0}, Items Sum = {1}\n" \
        "Max Item Date = {2}, Max Items = {3}\n" \
        "Max Amount Date = {4}, Max Amount = {5}".format(rm.impl.sum_amounts,
                                                         rm.impl.sum_items,
                                                         rm.impl.max_item_date,
                                                         rm.impl.max_item,
                                                         rm.impl.max_amount_date,
                                                         rm.impl.max_amount)
    rm.clear()
    print '\n', 30 * '-', '\n'
#    rm.test()


    print '\n', 30 * '-', '\n'
    rm2 = RecManip()
    rm2.importRecord('/home/jason/Py/Expenses/example_export.dat')
    
    print '\n', '=' * 40, '\n'
    print rm.impl.isExistence(date(2011, 1, 1))
    print rm.impl.isExistence(date(2011, 5, 1))
    dat = rm.findDates(date(2011, 4, 11), 100)
    for k in dat:
        print k, ' : ', len(dat[k])
    rm.clear()
    
    tem = BaseRecord('4', 3)
    rm.addItem(date(2008, 5, 1), tem)
    tem = BaseRecord('4', 3)
    rm.addItem(date(2009, 5, 1), tem)
    tem = BaseRecord('4', 3)
    rm.addItem(date(2010, 5, 1), tem)
    tem = BaseRecord('4', 3)
    rm.addItem(date(2012, 5, 1), tem)
    tem = BaseRecord('4', 3)
    rm.addItem(date(2013, 5, 1), tem)
    rm.exportRecord('/home/jason/Py/Expenses/example_export2.dat')
    
    

    print '调用过程用时为：{0:.3f}s'.format(time.time() - starttime)
