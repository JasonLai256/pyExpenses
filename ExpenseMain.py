#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
from decimal import Decimal
try:
    import cPickle as Pickle
except:
    import Pickle
import RecorManip
import ConfigManip
import RecParser as RP
import ErrorHandle as EH


def timecheck(date):
    """检查date的格式是否符合ISO格式 'yyyy-mm-dd' """
    if date[4] == '-' and date[7] == '-':
        return True
    return False
    

class Expense(object):
    def __init__(self):
        self.conf_m = ConfigManip.ConfigManip()
        self.rec_m = self.rec_unpickling()    # Records Manipulator
        self.projects = []

    def rec_pickling(self):
        file = open('/home/jason/Py/Expenses/records.dat', 'wb')
        Pickle.dump(self.rec_m, file, 2)

    def rec_unpickling(self):
        fname = '/home/jason/Py/Expenses/records.dat'
        if not os.path.getsize(fname):
            return RecorManip.RecorManip()
        else:
            picfile = open(fname)
            return Pickle.load(picfile)

    def addItem(self, time, baserec):
        if not timecheck(time):
            EH.valueError('time is not valid iso format.')
        self.rec_m.addItem(time, baserec)
        self.conf_m.setDefaultType(baserec)

    def figure_out(self, begin, end, parsers = []):
        """
        """
        starttime = time.time()
        
        data = self.rec_m.record_range(begin, end)
        parser = RP.MainParser(data)
        parser.extend(parsers)
#        return parser.parse()

        # 下面为测试用代码：
        ret = parser.parse()
        print '   ## 计算用时为：{0:.3f}s ##'.format(time.time() - starttime)
        return ret
        
        
    def importData(self, filename):
        self.rec_m.importRecord(filename)

    def exportData(self, filename):
        self.rec_m.exportRecord(filename)
        
        

if __name__ == '__main__':
    starttime = time.time()

    exp = Expense()
#    exp.importData('/home/jason/Py/Expenses/example.dat')
    cm = ConfigManip.ConfigManip()
    
    parsers = []
    parsers.append(RP.Amount_Stat())
    parsers.append(RP.Count_Stat())
    parsers.append(RP.General_Analys())
#    parsers.append(RP.Type_Filter(cm.type2num('ConsumingType', '交通')))
#    parsers.append(RP.Money_Filter(10))
#    parsers.append(RP.DaysInMonth_Filter([x for x in xrange(1, 32)]))
#    parsers.append(RP.MthsInYear_Filter([x for x in xrange(1, 13)]))
#    parsers.append(RP.DaysInWeek_Filter([x for x in xrange(0, 7)]))

    print '\n   ## 初始化用时为：{0:.3f}s ##'.format(time.time() - starttime)

    def display(btime, etime):
        global exp, parsers
        analy_res, stat_res, seq = exp.figure_out(btime, etime, parsers)
        print '{0} to {1} :'.format(btime, etime)
        for item in analy_res[0][1]:
            print '\t{0}  {1}  {2}%'.format(cm.num2type('ConsumingType', item[0]),
                                                    item[1],
                                                    item[2])
        print '\tsum = {0}, quantity = {1}, SeqLenght = {2}' \
            .format(stat_res[0][1], stat_res[1][1], len(seq))

    
#    display('2011-07-01', '2011-07-20')
#    display('2011-02-01', '2011-07-20')
#    display('2010-07-01', '2011-07-20')
#    display('2010-02-01', '2011-07-20')
#    display('2009-07-01', '2011-07-20')
#    display('2009-02-01', '2011-07-20')
#    display('2008-07-01', '2011-07-20')
#    display('2008-02-01', '2011-07-20')
#    display('2007-07-01', '2011-07-20')
#    display('2007-02-01', '2011-07-20')
#    display('2006-07-01', '2011-07-20')
    display('2006-02-01', '2011-07-20')
    display('2005-02-01', '2011-10-31')


#    ad = exp.allData()
    
#    exp.rec_pickling()
#    exp.exportData('/home/jason/Py/Expenses/example_export.dat')



    print '   ## 调用过程用时为：{0:.3f}s ##\n'.format(time.time() - starttime)
