#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
The format of seq -- data flow -- of RecorManip modure:

Sequence[date1, date2, date3, ... , dateN]  # dict
         --+---
           | (mapping) (date : storage)
           |
           +--> Storage[baserec1, baserec2, ... , baserecN]  # list
                        ---+----
                           |
                   +-------+
                   |
                   +--> BaseRecord(att1, att2, ... , attN)  # class
"""

from decimal import Decimal
from collections import deque
from datetime import date, timedelta

import ErrorHandle as EH
from utils import to_date


def asum(datas):
    """Calculate the sum of amount in sequence.
    """
    amount = 0.0
    # items structure is a tuple such as (date, rec_deque)
    for key in datas:
        amount += sum(record.amount for record in datas[key])
    #Note: Decimal use quantize() to ensure output precision.
    return Decimal(str(amount)).quantize(Decimal('1.00'))


class Parser(object):
    def __init__(self, parser_type = None):
        self.type = parser_type
        
    def parse(self):
        pass


class MainParser(Parser):
    def __init__(self, recgroup):
        self._records = recgroup            # data sequence
        self._ft_list = []            # filter list
        self._stat_list = []            # statistic list
        self._analy_list = []            # analysis list
        super(MainParser, self).__init__('mainparser')

    def parse(self):
        if not self._stat_list and not self._analy_list:
            # default strategy is use General_Analys to parse the records.
            self._analy_list.append(General_Analys())

        dealed_seq = self._filter()
        analy_result = self._analysis(dealed_seq)
        stat_result = self._statistic(dealed_seq)
        
        return analy_result, stat_result, dealed_seq

    def _filter(self):
        """filter data container."""
        if not self._ft_list:
            return self._records
        
        dealed_seq = self._records.copy()
        for parser in self._ft_list:
            dealed_seq = parser.parse(dealed_seq)
        return dealed_seq

    def _statistic(self, recgroup):
        """statistic data container."""
        retval = []
        for parser in self._stat_list:
            retval.append(parser.parse(recgroup))
        return retval

    def _analysis(self, recgroup):
        """analyze data container."""
        retval = []
        for parser in self._analy_list:
            retval.append(parser.parse(recgroup))
        return retval

    def append(self, parser):
        if parser.type == 'filter':
            self._ft_list.append(parser)
        elif parser.type == 'statistic':
            self._stat_list.append(parser)
        elif parser.type == 'analysis':
            self._analy_list.append(parser)
        else:
            EH.valueError("{0} is can't recognize.".format(parser.type))

    def extend(self, plist):
        for parser in plist:
            self.append(parser)

    def clear(self):
        self._ft_list = []
        self._stat_list = []
        self._analy_list = []

    def getchild(self):
        pass
    
        
    
class Amount_Stat(Parser):
    """Figure out the amount of money in data flow.
    @note: can specify a few subparser that use to filter some
           situation.
    """
    def __init__(self):
        super(Amount_Stat, self).__init__('statistic')

    def parse(self, recgroup):
        return 'Amount', asum(recgroup)


class Count_Stat(Parser):
    """Figure out the amount of records in data flow.
    @note: 是否应该 可选择是否返回Recs的具体项，待考虑。
    """
    def __init__(self):
        super(Count_Stat, self).__init__('statistic')

    def parse(self, recgroup):
        """Count the quantity of elements in sequence.
        """
        csum = sum(len(item) for item in recgroup.values())
        return 'Count', csum

    
class Type_Filter(Parser):
    """用于extract指定Type的Recores数据。"""
    def __init__(self, Optcode, AttrType='type'):
        self.optcode = Optcode
        self.atype = AttrType
        self._test()
        super(Type_Filter, self).__init__('filter')

    def parse(self, recgroup):
        if self.atype is 'type' and not isinstance(self.optcode, tuple):
            # BaseRecord.type is constructed to (maintype, subtype), is a
            # 2-tuple, this situation is just filter maintype of type.
            return self._type_filter(recgroup, ismaintype=True)
        else:
            return self._type_filter(recgroup)

    def _type_filter(self, recgroup, ismaintype=False):
        retval = {}
        for kdate, records in recgroup.items():
            for record in records:
                rtype = self._gettype(record, ismaintype)
                if rtype == self.optcode:
                    if not retval.has_key(kdate):
                        retval[kdate] = []
                    retval[kdate].append(record)
        return retval

    def _gettype(self, record, isMaintype):
        if isMaintype:
            return getattr(record, 'type')[0]
        else:
            return getattr(record, self.atype, None)

    def _test(self):
        pass


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

    def parse(self, recgroup):
        retval = {}
        for kdate, records in recgroup.items():
            for record in records:
                if self.start <= record.amount < self.stop:
                    if not retval.has_key(kdate):
                        retval[kdate] = []
                    retval[kdate].append(record)
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
        self.weekdays = self._test_and_correct(arglist)
        super(DaysInWeek_Filter, self).__init__('filter')

    def parse(self, recgroup):
        retval = {}
        for kdate, records in recgroup.items():
            if kdate.weekday() in self.weekdays:
                retval[kdate] = records
        return retval

    def _test_and_correct(self, daylist):
        for i in xrange(len(daylist)):
            daylist[i] = int(daylist[i])
            
        for item in daylist:
            if not 0 <= item <= 6:
                EH.valueError(
                    '{0} is not a correct number in day of weekdays.'.format(item)
                )
        return daylist


class DaysInMonth_Filter(Parser):
    """Filter the days in day of month that specified by arglist.
    """
    def __init__(self, arglist):
        self.days = self._test_and_correct(arglist)
        super(DaysInMonth_Filter, self).__init__('filter')

    def parse(self, recgroup):
        retval = {}
        for kdate, records in recgroup.items():
            if kdate.day in self.days:
                retval[kdate] = records
        return retval

    def _test_and_correct(self, daylist):
        for i in xrange(len(daylist)):
            daylist[i] = int(daylist[i])
            
        for item in daylist:
            if not 1 <= item <= 31:
                EH.valueError(
                    '{0} is not a correct number in day of months.'.format(item)
                )
        return daylist


class MthsInYear_Filter(Parser):
    """Filter the months in year that specified by arglist.
    """
    def __init__(self, arglist):
        self.mths = self._test_and_correct(arglist)
        super(MthsInYear_Filter, self).__init__('filter')

    def parse(self, recgroup):
        retval = {}
        for kdate, records in recgroup.items():
            if kdate.month in self.mths:
                retval[kdate] = records
        return retval

    def _test_and_correct(self, mthlist):
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

    @note: the format of return values is:
                item (type, amount, percentage)
    """
    def __init__(self):
        super(General_Analys, self).__init__('analysis')

    def parse(self, recgroup):
        valdict = {}
        for kdate, records in recgroup.items():
            for record in records:
                # this parser just analysis the maintype of BaseRecord.type
                # so that use record.type[0] to be the key of dict followed.
                key = record.type[0]
                if not valdict.has_key(key):
                    valdict[key] = [0.0, None]

                valdict[key][0] += record.amount

        asum = sum(item[0] for item in valdict.values())
        self._figure_percentage(valdict, asum)

        retval = self._make_list(valdict)
        retval.sort(key=lambda x: x[1])
        return 'Generally Analyse', retval

    def _figure_percentage(self, valdict, asum):
        for key in valdict.keys():
            percent = valdict[key][0] / asum * 100
            valdict[key][1] = '{0:.2f}'.format(percent)  # convert to formated str

    def _make_list(self, valdict):
        """From dictionary struc transform to list struc."""
        retlist = []
        for key in valdict.keys():
            elem = (key,
                    Decimal(str(valdict[key][0])).quantize(Decimal('1.00')),
                    valdict[key][1])
            retlist.append(elem)
        return retlist


# ============================================================
# ** following is parsing functions for Expense's Project.
# 
# ============================================================
PROJECT_TARGET = 'The amount of project target is {0}.'
PROJECT_START_DATE = 'The project was start at {0}.'
REST_OF_GOAL = 'For accomplish project target, remain {0}.'
AVERAGE_OF_REC = 'The average of each amount of registering record is {0}.'
PAST_DATES = 'From project start, had {0} days was past.'
REMAIN_DATES = 'To project end, had {0} days is remain.'
HAS_ACCOMPLISH = 'The project was accomplished at {0}.'

HAS_QUARTER = 'The quarter target amount of project had satified at {0}.'
HAS_HALF = 'The half target amount of project had satified at {0}.'
HAS_THREEQUARTERS = 'The three-quarter target amount of project had satified at {0}.'
IS_RECURSION = 'Project recursion is enable, recursive period is {0} days.'

    
def consumingProjectParse(data):
    retseq = []
    statdict = data['p_statdict']

    restOfGoal = data['p_target_amount'] - data['p_accumt_amount']
    averageOfRec = data['p_accumt_amount'] / data['p_recs_amount']
    pastDates = (date.today() - to_date(data['p_start_time'])).days
    remainDates = data['p_period'] - pastDates

    # figure out the basic infomation of project.
    templist = [
        PROJECT_TARGET.format(data['p_target_amount']),
        PROJECT_START_DATE.format(data['p_start_time']),
        REST_OF_GOAL.format(restOfGoal),
        AVERAGE_OF_REC.format(averageOfRec),
        PAST_DATES.format(pastDates),
        REMAIN_DATES.format(remainDates)
    ]
    retseq.extend(templist)

    # figure out the milestone of project target.
    _milestone_check(
        data['p_accumt_amount'], data['p_target_amount'], statdict
    )
    # judge situations of project to process 
    if data['p_accomplish_date']:
        retseq.append(
            HAS_ACCOMPLISH.format(data['p_accomplish_date'])
        )
    elif statdict['hasThreeQuarters']:
        retseq.append(
            HAS_THREEQUARTERS.format(statdict['DateOfThreeQuarters'])
        )
    elif statdict['hasHalf']:
        retseq.append(
            HAS_HALF.format(statdict['DateOfHalf'])
        )
    elif statdict['hasQuarter']:
        retseq.append(
            HAS_QUARTER.format(statdict['DateOfQuarter'])
        )

    # if project recursion is enable.
    if data['p_recursion']:
        retseq.append(
            IS_RECURSION.format(data['p_period'])
        )

    return retseq

def _milestone_check(accumulated, target, statdict):
    if not statdict['hasQuarter']:
        if accumulated >= (target / 4):
            statdict['hasQuarter'] = True
            statdict['DateOfQuarter'] = date.today().isoformat()
    if not statdict['hasHalf']:
        if accumulated >= (target / 2):
            statdict['hasHalf'] = True
            statdict['DateOfHalf'] = date.today().isoformat()
    if not statdict['hasThreeQuarters']:
        if accumulated >= (target * 3 / 4):
            statdict['hasThreeQuarters'] = True
            statdict['DateOfThreeQuarters'] = date.today().isoformat()
