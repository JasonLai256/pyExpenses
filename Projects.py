#! /usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import date, timedelta


def create_date(self, da):
    """设定da的格式为'yyyy-mm-dd'."""
    if isinstance(da, date):
        return da
    elif isinstance(da, str):
        y = int(da[:4])
        m = int(da[5:7])
        d = int(da[8:])
        return date(y, m, d)
    else:
        EH.valueError('date ({0}) format error.'.format(str(da)))


class Project(object):
    def __init__(self, project_type = None):
        """Note that status is numeric code, have following meaning:
                111 - Default status that nothing happens.
                222 - Project purpose is accomplish.
                333 - Project period is past and ready to terminate.
        """
        self.type = project_type
        self.status = 111

    def register(self, baserec):
        pass

    def report(self):
        print "There is a Expenses project report."


class Consuming_Project(Project):
    def __init__(self, Target, Period, Type = None,
                   Optcode = None, Recursion = False):
        self.target_amount = Target
        self.period = timedelta(int(Period))
        self.ptype = Type
        self.optcode = Optcode
        self.accum_amount = 0.0    # accumulated amount

        self.accomplish_date = None    # project purpose's accomplishing date
        self.start_time = date.today()    # time of project start
        self.recursion = Recursion

        self.progress_hint = []
        self.analysis_result = []

        super(Consuming_Project, self).__init__('record')

    def register(self, date_s, baserec):
        """Register a specific record in the project.
        """
        date_v = create_date(date_s)
        date_state = self._date_checker(date_v)
        # date_v not in the period (state != 0), do nothing and return        
        if date_state: return

        if not self._type_checker(baserec): return
        self.accum_amount += baserec.amount
        self._amount_checker()

    def register_del(self, date_s, baserec):
        date_v = create_date(date_s)
        date_state = self._date_checker(date_v)
        # date_v not in the period (state != 0), do nothing and return
        if date_state: return            

        if not self._type_checker(baserec): return
        self.accum_amount -= baserec.amount
        self._amount_checker()

    def register_upd(self, date_s, baserec, newrec):
        date_v = create_date(date_s)
        date_state = self._date_checker(date_v)
        # date_v not in the period (state != 0), do nothing and return
        if date_state: return

        if not self._type_checker(baserec): return
        self.accum_amount += (baserec.amount - newrec.amount)
        self._amount_checker()
        
    def report(self, rec_m):
        pass

    def report_export(self, rec_m):
        pass

    def _date_checker(self, date_v):
        """Judge a few situation of date of record and handle it."""
        if date.today() >= self.start_time + self.period:
            # Today is out of period, handle all situation.
            if self.recursion:
                # Init the recursive situation.
                self._recursive_init_handler()
            else:
                self._finish_handler()
        
        if date_v < self.start_time:
            # The date of record is not in the period.
            return -1
        elif date_v >= self.start_time + self.period:
            # The date of record is out of period.
            return 1
        else:
            # The date of record is in the period.
            return 0

    def _type_checker(self, baserec):
        if not self.ptype or not self.optcode:
            return False

        # 这里可以使用表驱动法去实现...
        # To be continue...

    def _amount_checker(self):
        if self.accum_amount >= self.target_amount:
            if not self.accomplish_date:
                # accomplish_date not have record.
                self.accomplish_date = date.today()
                self.status = 222
        else:
            if self.accomplish_date:
                # Accomplish_date had been recorded.
                self.accomplish_date = None
                self.status = 111
            # always analyze the data if project not accomplish.
            self._analyze()

    def _analyze(self):
        pass

    def _init_handler(self):
        pass

    def _finish_handler(self):
        # some record jobs...
        self.status = 333

    def _recursive_init_handler(self):
        # some record jobs...
        self.status = 111
        self.accum_amount = 0.0
        self.accomplish_date = None
        self.start_time = self.start_time + self.period:



if __name__ == '__main__':
    pass
