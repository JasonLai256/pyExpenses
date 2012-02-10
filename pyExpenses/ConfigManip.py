#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
    pyExpenses.ConfigManip
    ~~~~~~~~~~~~~~~~~~~~~~

    Implements the configuration related objects.

    :copyright: (c) 2012 by Jason Lai.
    :license: BSD, see LICENSE for more details.
"""

import json
import os
from os.path import abspath, join, dirname

import ErrorHandle as EH

def _importObj(filename):
    path = join(abspath(dirname(__file__)), filename)
    
    if not os.path.isfile(path):
        raise IOError
    if not os.path.getsize(path):
        # the size of file is zero that contain nothing
        with open(path, 'w') as tempfile:
            print '\n** ', path, '\n'
            json.dump(dict(), tempfile)   # create a empty json dict

    return json.load(open(path))

def _exportObj(obj, filename, path=None):
    if path:
        fpath = os.path.join(path, filename)
    else:
        fpath = os.path.join(Config.getInfo('path'), filename)
    with open(fpath, 'w') as jfile:
        json.dump(obj, jfile, sort_keys=True, indent=4)

def _updOrder(item, seq):
    index = seq.index(item)
    if index == 0:
        # don't need to change order because item is the first element of seq
        return seq
    else:
        return seq[index:index+1] + seq[:index] + seq[index+1:]

def _addTypeOpt(obj, mtype, subtype):
    """If don't understand the logic of this function, could look up
    the config.json file for clear mind.
    """
    if obj['Type']['types'].has_key(mtype):
        if subtype not in obj['Type']['types'][mtype]:
            obj['Type']['types'][mtype].append(subtype)
    else:
        # Note: before assignment subtype should convert to a list firstly.
        # Also note that subtype could't use list() to init because subtype
        # is a str or unicode object.
        obj['Type']['types'][mtype] = [subtype]

def _delTypeOpt(obj, mtype, subtype):
    if obj['Type']['types'].has_key(mtype):
        if subtype in obj['Type']['types'][mtype]:
            obj['Type']['types'][mtype].remove(subtype)
            if not obj['Type']['types'][mtype]:
                del obj['Type']['types'][mtype]
                

class ConfiMeta(type):
    def __new__(cls, name, bases, dict):
        try:            
            dict['objfile'] = 'config.json'
            dict['buffile'] = 'databuf.json'
            dict['obj'] = _importObj(filename=dict['objfile'])
            # A storing object that contain the datas of project's buffer
            # and records buffer by json format.
            dict['bufobj'] = _importObj(filename=dict['buffile'])

            dict['obj']['BaseInfo']['path'] = abspath(dirname(__file__))
        except IOError:
            EH.ioError(
                "file ./confi.json not exist, can't initialise program."
            )
        return super(cls, ConfiMeta).__new__(cls, name, bases, dict)

class Config(object):
    __metaclass__ = ConfiMeta
    
    @classmethod
    def getInfo(cls, option):
        return cls.obj['BaseInfo'][option]
            
    @classmethod
    def setInfo(cls, option, value):
        """Set the given option to the specifit value for BaseInfo section.
        @note: there are not to check the value is valid or not, so need
               to ensure value is valid before invoke this method.
        """
        if not cls.obj['BaseInfo'].has_key(option):
            EH.attrError(
                'Expense info has not "{0}" option.'.format(option)
            )
        cls.obj['BaseInfo'][option] = value
        _exportObj(cls.obj, cls.objfile)

#    @classmethod
#    def secionts(cls):
#        return cls.obj.keys()
            
    @classmethod
    def getOptions(cls, section):
        if section not in ['Type', 'Payment', 'Currency', 'Tag']:
            EH.valueError('section value is invalid.')
        retval = []
        if section == 'Type':
            for t in cls.obj[section]['type_order']:
                retval.append(
                    (t, cls.obj['Type']['types'][t])
                )
        else:
            retval = cls.obj[section]['types']
        return retval

    @classmethod
    def addOption(cls, section, val):
        """If val is not exist then create a new one that suit to the
        situation of section. On the other hand, if val is already exist
        nothing will happends.
        """
        if section not in ['Type', 'Payment', 'Currency', 'Tag']:
            EH.valueError('section value is invalid.')
        if section == 'Type':
            _addTypeOpt(cls.obj, mtype=val[0], subtype=val[1])
        else:
            if val not in cls.obj[section]['types']:
                cls.obj[section]['types'].append(val)
        _exportObj(cls.obj, cls.objfile)

    @classmethod
    def delOption(cls, section, val):
        if section not in ['Type', 'Payment', 'Currency', 'Tag']:
            EH.valueError('section value is invalid.')
        if section == 'Type':
            _delTypeOpt(cls.obj, mtype=val[0], subtype=val[1])
        else:
            if val in cls.obj[section]['types']:
                cls.obj[section]['types'].remove(val)
        _exportObj(cls.obj, cls.objfile)

    @classmethod
    def getDefaults(cls):
        """This method offer the default options of Type, Payment, Currency
        and Tag.
        """
        retval = []
        retval.append(cls.obj['Type']['default'])
        retval.append(cls.obj['Payment']['default'])
        retval.append(cls.obj['Currency']['default'])
        retval.append(cls.obj['Tag']['default'])
        return retval

    @classmethod
    def setDefault(cls, baserec):
        """This method serve for the options include Type, Payment, Currency
        and Tag, provide recording functionality of option.

        @Note: types showing strategy is last use first show, so we need to
        update the order each time.
        """
        cls.obj['Type']['default'] = baserec.type
        cls.obj['Payment']['default'] = baserec.payment
        cls.obj['Currency']['default'] = baserec.currency
        cls.obj['Tag']['default'] = baserec.tag

        cls.obj['Type']['type_order'] = _updOrder(
            cls.obj['Type']['default'][0], cls.obj['Type']['type_order']
        )
        cls.obj['Payment']['types'] = _updOrder(
            cls.obj['Payment']['default'], cls.obj['Payment']['types']
        )
        cls.obj['Currency']['types'] = _updOrder(
            cls.obj['Currency']['default'], cls.obj['Currency']['types']
        )
        cls.obj['Tag']['types'] = _updOrder(
            cls.obj['Tag']['default'], cls.obj['Tag']['types']
        )
        _exportObj(cls.obj, cls.objfile)

    @classmethod
    def getProjectBuffer(cls):
        if not cls.bufobj.has_key('ProjectBuf'):
            cls.bufobj['ProjectBuf'] = {}
        return cls.bufobj['ProjectBuf']

    @classmethod
    def setProjectBuffer(cls, bufobj):
        cls.bufobj['ProjectBuf'] = bufobj
        _exportObj(cls.bufobj, cls.buffile)

    @classmethod
    def getRecordBuffer(cls):
        if not cls.bufobj.has_key('RecordBuf'):
            cls.bufobj['RecordBuf'] = []
        return cls.bufobj['RecordBuf']

    @classmethod
    def setRecordBuffer(cls, bufobj):
        cls.bufobj['RecordBuf'] = bufobj
        _exportObj(cls.bufobj, cls.buffile)
