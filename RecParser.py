#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
The format of seq -- data flow -- of RecorManip modure:

Sequence[conta1, conta2, conta3, ... , contaN]  # deque
         --+---
           |
           +--> Container(date, storage)  # tuple
                                ---+---
                                   |
               +-------------------+
               |
               +--> Storage[baserec1, baserec2, ... , baserecN]  # deque
                            ---+----
                               |
                   +-----------+
                   |
                   +--> BaseRecord(att1, att2, ... , attN)  # class
"""

from decimal import Decimal
from collections import deque
from datetime import date
import ErrorHandle as EH


def asum(dataseq):
    """Calculate the sum of amount in sequence.
    """
    amount = 0.0
    # items structure is a tuple such as (date, rec_deque)
    for item in dataseq:        
        amount += sum(record.amount for record in item[1])
    #Note: Decimal use quantize() to ensure output precision.
    return Decimal(str(amount)).quantize(Decimal('1.00'))

def safe_append(seq, date_s, value):
    """This func can detect different conditions that may happen on
    filter parser append data in new sequence and perform some procedure.
    
    @note: about the explicit description of Seq format, could lookup
    upon this file.
    """
    if not len(seq):
        # Is seq empty?
        seq.append( (date_s, deque()) )
        seq[0][1].append(value)
        return
        
    if seq[-1][0] == date_s:
        # Date is already exist in seq. Note that Seq format is already
        # sorted, we could use this feature to judge.
        seq[-1][1].append(value)
    else:
        seq.append( (date_s, deque()) )
        seq[-1][1].append(value)


class Parser(object):
    def __init__(self, parser_type = None):
        self.type = parser_type
        
    def parse(self):
        pass


class MainParser(Parser):
    def __init__(self, dataseq):
        self.__d_seq = dataseq            # data sequence
        self.__ft_list = []            # filter list
        self.__stat_list = []            # statistic list
        self.__analy_list = []            # analysis list
        super(MainParser, self).__init__('mainparser')

    def parse(self):
        if not self.__stat_list and not self.__analy_list:
            # default strategy is use General_Analys to parse the fsequence.
            self.__analy_list.append(General_Analys())

        dealed_seq = self._filter()
        analy_result = self._analysis(dealed_seq)
        stat_result = self._statistic(dealed_seq)
        
        return analy_result, stat_result, dealed_seq

    def _filter(self):
        """filter data sequence."""
        if not self.__ft_list:
            return self.__d_seq
        
        dealed_seq = self.__d_seq
        for parser in self.__ft_list:
            dealed_seq = parser.parse(dealed_seq)
        return dealed_seq

    def _statistic(self, dataseq):
        """statistic data sequence."""
        retval = []
        for parser in self.__stat_list:
            retval.append(parser.parse(dataseq))
        return retval

    def _analysis(self, dataseq):
        """analyze data sequence."""
        retval = []
        for parser in self.__analy_list:
            retval.append(parser.parse(dataseq))
        return retval

    def append(self, parser):
        if parser.type == 'filter':
            self.__ft_list.append(parser)
        elif parser.type == 'statistic':
            self.__stat_list.append(parser)
        elif parser.type == 'analysis':
            self.__analy_list.append(parser)
        else:
            EH.valueError("{0} is can't recognize.".format(parser.type))

    def extend(self, plist):
        for par in plist:
            self.append(par)

    def clear(self):
        self.__ft_list = deque()
        self.__stat_list = deque()
        self.__analy_list = deque()

    def getchild(self):
        pass
    
        
    
class Amount_Stat(Parser):
    """统计data流中的金额总量。
    @note: can specify a few subparser that use to filter some
           situation.
    """
    def __init__(self):
        super(Amount_Stat, self).__init__('statistic')

    def parse(self, dataseq):
        return 'Amount', asum(dataseq)


class Count_Stat(Parser):
    """统计data流中的Recore个数。
    @note: 是否应该 可选择是否返回Recs的具体项，待考虑。
    """
    def __init__(self):
        super(Count_Stat, self).__init__('statistic')

    def parse(self, dataseq):
        """Count the quantity of elements in sequence.
        """
        csum = sum(len(item[1]) for item in dataseq)
        return 'Count', csum

    
class Type_Filter(Parser):
    """用于extract指定Type的Recores数据。"""
    def __init__(self, Optcode, AttrType = 'ConsumingType'):
        self.optcode = str(Optcode)
        self.attr = AttrType
        super(Type_Filter, self).__init__('filter')

    def parse(self, dataseq):
        retval = deque()
        for item in dataseq:
            for record in item[1]:
                if record.getAttr(self.attr) == self.optcode:
                    safe_append(retval, item[0], record)
        return retval


class Money_Filter(Parser):
    """用于ectract指定金额范围内的Recores数据。"""
    def __init__(self, range1, range2 = None):
        if range2:
            self.start = float(range1)
            self.stop = float(range2)
        else:
            self.start = 0.0
            self.stop = float(range1)

        self._test()
        super(Money_Filter, self).__init__('filter')

    def parse(self, dataseq):
        retval = deque()
        for item in dataseq:
            for record in item[1]:
                if self.start <= record.amount and \
                record.amount <= self.stop:
                    safe_append(retval, item[0], record)
        return retval

    def _test(self):
        if self.start < 0 or self.stop < 0 or \
        self.stop < self.start:
            EH.valueError("start number({0}) and stop number({1}) has" \
                              "value problem.".format(self.start, self.stop))

    
class PT_Filter(Parser):
    pass


class DaysInWeek_Filter(Parser):
    """Filter the days in weekday that specified by arglist.

    @note: about the days number, where Monday is 0 and Sunday is 6.
    """
    def __init__(self, arglist):
        self.weekdays = self._corre_and_test(arglist)
        super(DaysInWeek_Filter, self).__init__('filter')

    def parse(self, dataseq):
        retval = deque()
        for item in dataseq:
            da = self._createDate(item[0])
            if da.weekday() in self.weekdays:
                retval.append(item)
        return retval

    def _corre_and_test(self, daylist):
        for i in xrange(len(daylist)):
            int(daylist[i])
            
        for item in daylist:
            if not 0 <= item <= 6:
                EH.valueError('{0} is not a correct number in weekday.' \
                                  .format(item))
        return daylist

    def _createDate(self, da):
        """设定da的格式为'yyyy-mm-dd'."""
        if type(da) == type(date.today()):
            return da
        
        y = int(da[:4])
        m = int(da[5:7])
        d = int(da[8:])
        return date(y, m, d)


class DaysInMonth_Filter(Parser):
    """Filter the days in day of month that specified by arglist.
    """
    def __init__(self, arglist):
        self.days = self._corre_and_test(arglist)
        super(DaysInMonth_Filter, self).__init__('filter')

    def parse(self, dataseq):
        retval = deque()
        for item in dataseq:
            day = int(item[0][8:])
            if day in self.days:
                retval.append(item)
        return retval

    def _corre_and_test(self, daylist):
        for i in xrange(len(daylist)):
            int(daylist[i])
            
        for item in daylist:
            if not 1 <= item <= 31:
                EH.valueError('{0} is not a correct number in day of months.' \
                                  .format(item))
        return daylist


class MthsInYear_Filter(Parser):
    """Filter the months in year that specified by arglist.
    """
    def __init__(self, arglist):
        self.mths = self._corre_and_test(arglist)
        super(MthsInYear_Filter, self).__init__('filter')

    def parse(self, dataseq):
        retval = deque()
        for item in dataseq:
            mth = int(item[0][5:7])
            if mth in self.mths:
                retval.append(item)
        return retval

    def _corre_and_test(self, mthlist):
        for i in xrange(len(mthlist)):
            int(mthlist[i])
            
        for item in mthlist:
            if not 1 <= item <= 12:
                EH.valueError('{0} is not a correct number in months.' \
                                  .format(item))
        return mthlist


class General_Analys(Parser):
    """There are provides some general functionality for analysis 
    include figure out amount of different consuming type and the
    percentage of those amount.

    @note: unit export format is:
                item [csm_type, amount, percentage]
    """
    def __init__(self):
        super(General_Analys, self).__init__('analysis')

    def parse(self, dataseq):
        valdict = {}
        for item in dataseq:
            for record in item[1]:
                if not valdict.has_key(record.csm_type):
                    valdict[record.csm_type] = [0.0, None]

                valdict[record.csm_type][0] += record.amount

        asum = sum(item[0] for item in valdict.values())
        self._figure_percentage(valdict, asum)

        retval = self._make_list(valdict)
        retval.sort(key=lambda x: x[1])
        return 'Generally Analyse', retval

    def _figure_percentage(self, valdict, asum):
        for key in valdict.keys():
            percent = valdict[key][0] / asum * 100
            valdict[key][1] = percent

    def _make_list(self, valdict):
        """From dictionary struc transform to list struc."""
        retlist = []
        for key in valdict.keys():
            elem = (key,
                    Decimal(str(valdict[key][0])).quantize(Decimal('1.00')),
                    valdict[key][1])
            retlist.append(elem)
        return retlist
