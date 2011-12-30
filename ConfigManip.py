#! /usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import os
import ErrorHandle as EH


def _importObj():
    with open('/home/jason/Py/Expenses/config.json') as fil:
        return json.load(fil)

def _exportObj():
    with open('/home/jason/Py/Expenses/config.json', 'w') as fil:
        json.dump(self.obj, fil, indent = 4)


class ConfiMeta(type):
    def __new__(cls, name, bases, dict):
        try:
            dict['obj'] = _importObj()
        except IOError:
            EH.ioerror(
                "file ./confi.json not exist, can't initialise program."
            )
        return super(cls, ConfiMeta).__new__(cls, name, bases, dict)

class Config(object):
    __metaclass__ = ConfiMeta
    
    @classmethod
    def secionts(cls):
        return cls.obj.keys()

    @classmethod
    def getInfo(cls, option):
        pass
            
    @classmethod
    def setInfo(cls, option, value):
        """Set the given option to the specifit value for BaseInfo section.
        @note: there are not to check the value is valid or not, so need
               to ensure value is valid before invoke this method.
        """
        pass
            
    @classmethod
    def getOptions(cls, section):
        return cls.obj.get(section, dict()).keys()

    @classmethod
    def setOption(cls, section, valtype, newval):
        """
        @note: if x not exist then create a new one that suit to the
        situation of section.
        """
        pass

    @classmethod
    def getDefaultType(cls):
        """This method only serve for ConsumingType, PaymentType and
        ConsumingCatagory sections that provided type recording
        functionality.
        """
        retval = []
        
        return retval

    @classmethod
    def setDefaultType(cls, baserec):
        """This method only serve for ConsumingType, PaymentType and
        ConsumingCatagory sections that provided type recording
        functionality.
        """
        pass

    @classmethod
    def num2type(cls, section, num):
        """Transform the Number to correctly maped Type.
        """
        tnum = str(num)
        
        if not cls.obj.has_key(section):
            EH.valueError('No Section Error: {0}'.format(section))
        if not cls.obj[section].has_key(tnum):
            EH.valueError('{0} is not in the options'.format(num))
            
        return cls.obj[section][tnum]

    @classmethod
    def type2num(cls, section, Type):
        """Transform the Type to correctly maped Number.
        """
        Type = unicode(Type, encoding='UTF-8')
        if not cls.obj.has_key(section):
            EH.valueError('No Section Error: {0}'.format(section))

        for num in cls.obj[section]:
            if Type == cls.obj[section][num]:
                return int(num)
        else:
            EH.valueError(
                '{0} is not a valid type.'.format(Type)
            )


if __name__ == '__main__':
    cm = Config
    print cm.num2type('ConsumingType', '5')
    print cm.type2num('ConsumingType', '食物')
    print cm.num2type('PaymentType', '2')
    print cm.type2num('PaymentType', '现金')
    print cm.num2type('Tag', '0')
    print cm.type2num('Tag', '商务')
