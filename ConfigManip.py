#! /usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import ErrorHandle as EH

class ConfigManip(object):
    def __init__(self):
        try:
            self.obj = self._importObj()
        except IOError:
            print "file ./confi.json not exist, can't initialise program."
            sys.exit(1)

    def _importObj(self):
        with open('/home/jason/Py/Expenses/config.json') as fil:
            return json.load(fil)

    def _exportObj(self):
        with open('/home/jason/Py/Expenses/config.json', 'w') as fil:
            json.dump(self.obj, fil)

    def secionts(self):
        return self.obj.keys()

    def getInfo(self, option):
        pass
            
    def setInfo(self, option, value):
        """Set the given option to the specifit value for BaseInfo section.
        @note: there are not to check the value is valid or not, so need
               to ensure value is valid before invoke this method.
        """
        pass
            
    def getOptions(self, section):
        return self.obj.get(section, dict()).keys()

    def setOption(self, section, valtype, newval):
        """
        @note: if x not exist then create a new one that suit to the
        situation of section.
        """
        pass

    def getDefaultType(self):
        """This method only serve for ConsumingType, PaymentType and
        ConsumingCatagory sections that provided type recording
        functionality.
        """
        retval = []
        
        return retval

    def setDefaultType(self, baserec):
        """This method only serve for ConsumingType, PaymentType and
        ConsumingCatagory sections that provided type recording
        functionality.
        """
        pass

    def num2type(self, section, num):
        """Transform the Number to correctly maped Type.
        """
        tnum = str(num)
        if not self.obj.has_key(section):
            EH.valueError('No Section Error: {0}'.format(section))
            
        if not self.obj[section].has_key(tnum):
            EH.valueError('{0} is not in the options'.format(num))
        return self.obj[section][tnum]

    def type2num(self, section, Type):
        """Transform the Type to correctly maped Number.
        """
        Type = unicode(Type, encoding='UTF-8')
        if not self.obj.has_key(section):
            EH.valueError('No Section Error: {0}'.format(section))

        for numkey in self.obj[section]:
            if Type == self.obj[section][numkey]:
                return int(numkey)
        else:
            EH.valueError('{0} is not a valid type. {1}'.format(Type))


if __name__ == '__main__':
    cm = ConfigManip()
    print cm.num2type('ConsumingType', '5')
    print cm.type2num('ConsumingType', '食物')
    print cm.num2type('PaymentType', '2')
    print cm.type2num('PaymentType', '现金')
    print cm.num2type('Tag', '0')
    print cm.type2num('Tag', '商务')
    
    
