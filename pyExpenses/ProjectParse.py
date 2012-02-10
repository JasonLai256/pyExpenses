#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
    pyExpenses.ProjectParse
    ~~~~~~~~~~~~~~~~~~~~~~~

    Implement the parsing functions for Projects.

    :copyright: (c) 2012 by Jason Lai.
    :license: BSD, see LICENSE for more details.
"""

from datetime import date, timedelta

from utils import to_date


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
