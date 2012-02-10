#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
    pyExpenses.Projects
    ~~~~~~~~~~~~~~~~~~~

    Implements the project's object for pyExpenses.

    :copyright: (c) 2012 by Jason Lai.
    :license: BSD, see LICENSE for more details.
"""

from datetime import date, timedelta
from ProjectParse import consumingProjectParse
from utils import to_date


class Project(object):
    def __init__(self, project_type = None):
        """Note that status is described to numeric code, has following
        situations:
                111 - Default status that nothing happens.
                222 - Project purpose is accomplish.
                333 - Project period was past, new record will not register.
                444 - Project had error occurs can't to continue process.
                555 - Some situation have happened need to focus.
        """
        self.p_type = project_type
        self.p_status = 111

    def register(self):
        pass

    def report(self):
        """There is a infomation report of Expenses project that exist
        in all project subclass.
        Note that self.p_progress_info should be a iterable sequence.
        """
        return self.p_progress_info

    def export_to_dict(self):
        retval = {}
        for key in self.__dict__:
            # the second expr is judge whether the value of key is None
            if key == 'p_start_time':
                retval[key] = self.__dict__[key].isoformat()
            elif key == 'p_period':
                retval[key] = self.__dict__[key].days
            elif key.startswith('p_'):
                retval[key] = self.__dict__[key]
        return retval

    def import_from_dict(self, importDict):
        for key in importDict:
            if key == 'p_start_time':
                self.__dict__[key] = to_date(importDict[key])
            elif key == 'p_period':
                self.__dict__[key] = timedelta(importDict[key])
            elif key.startswith('p_'):
                self.__dict__[key] = importDict[key]


class ConsumingProject(Project):
    def __init__(self, Target=-1, Bdate=date(1970, 1, 1), Period=0, 
                   Type = '', Optcode = '', Recursion = False):
        self.p_target_amount = float(Target)
        self.p_start_time = Bdate    # date of project started
        self.p_period = timedelta(int(Period))
        self.p_typename = Type    # a type name of BaseRecord attribute
        self.p_optcode = Optcode
        self.p_recursion = Recursion

        self._init_handler()
        super(ConsumingProject, self).__init__(project_type='statistic')

    def register(self, rdate, baserec, newrec=None, act='add'):
        """Register infomations of the specific record in the project for
        add, delete and update.
        """
        # the meaning of those status code described in this module above.
        # Note that these four status may have differently procesing
        # procedure in following operation inside.
        if self.p_status not in (111, 222, 555):
            return
        
        try:
            self._register_check(rdate, baserec)
        except ValueError:
            return
        
        self._update(rdate, baserec, newrec, act)
        self._target_check()

    def _update(self, rdate, baserec, newrec, act):
        """update infomation of amount for the project
        """
        if act == 'add':
            self.p_accumt_amount += baserec.amount
            self.p_recs_amount += 1
        elif act == 'del':
            self.p_accumt_amount -= baserec.amount
            self.p_recs_amount -= 1
        elif act == 'udp':
            self.p_accumt_amount += (baserec.amount - newrec.amount)
        else:
            # do nothing
            pass

    def _register_check(self, rdate, baserec):
        if not self._date_checke(rdate):
            # rdate not in the period (state != 0), raise Error to return
            raise ValueError
        if not self._type_checke(baserec):
            # baserec type is not match self.optcode, raise Error to return
            raise ValueError

    def _date_checke(self, rdate):
        """Judge a few situations of date of record and handle it.
        """
        if date.today() >= self.p_start_time + self.p_period:
            # Today is out of period, handle all situation.
            if self.p_recursion:
                # Init the recursive situation.
                self._recursive_init()
            else:
                self._finish()
        
        if self.p_start_time <= rdate < self.p_start_time + self.p_period:
            # The date of record is in the period.
            return True
        else:
            # The date of record is not in the period.
            return False

    def _type_checke(self, baserec):
        """Check self.typename of baserec whether match the self.optcode.
        Note that self.typename and self.optcode may not was specified that
        meant any type of consuming could be record in this project, and
        this function just return True and do nothing.
        """
        if not self.p_typename or not self.p_optcode:
            return True

        if self.p_typename == 'type' and not isinstance(self.p_optcode, tuple):
            # BaseRecord.type is constructed to (maintype, subtype), is a
            # 2-tuple, this situation is just filter maintype of type.
            if getattr(baserec, self.p_typename)[0] == self.p_optcode:
                return True
            else:
                return False

        # general situations solving
        if getattr(baserec, self.p_typename) == self.p_optcode:
            return True
        else:
            return False

    def _target_check(self):
        if self.p_accumt_amount >= self.p_target_amount:
            if not self.p_accomplish_date:
                # accomplish_date not had record.
                self.p_accomplish_date = date.today().isoformat()
                self.p_status = 222
        else:
            if self.p_accomplish_date:
                # Accomplish_date had been recorded.
                self.p_accomplish_date = ''
                self.p_status = 111
        # always analyze the data
        self._analyze()

    def _analyze(self):
        """
        """
        data = self.export_to_dict()
        self.p_progress_info = consumingProjectParse(data)

    def _init_handler(self):
        self.p_accumt_amount = 0.0    # accumulated amount
        self.p_recs_amount = 0    # amount of records were registered in project
        self.p_accomplish_date = ''    # accomplishing date of project purpose

        self.p_info_history = {}
        self.p_progress_info = []
        
        self.p_statdict = dict(
            hasQuarter = False,
            hasHalf = False,
            hasThreeQuarters = False,
            DateOfQuarter = '',
            DateOfHalf = '',
            DateOfThreeQuarters = ''
        )

    def _recursive_init(self):
        self.p_status = 111
        self.p_info_history[self.p_start_time] = self.p_progress_info
        self.p_start_time = self.p_start_time + self.p_period
        self._init_handler()

    def _finish(self):
        self.p_status = 333
