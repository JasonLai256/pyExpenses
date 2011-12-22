#! /usr/bin/env python
# -*- coding:utf-8 -*-

from ConfigParser import SafeConfigParser
import sys
import ErrorHandle as EH

class ConfigManip:
    def __init__(self):
        self.cp = SafeConfigParser()
        try:
            self.cp.readfp(open('/home/jason/Py/Expenses/config.ini'))
        except IOError:
            print 'file ./confi.ini not exist, can not initialise program.'
            sys.exit(1)

    def secionts(self):
        return self.cp.sections()

    def getInfo(self, option):
        return self.cp.get('BaseInfo', option)
            
    def setInfo(self, option, value):
        """Set the given option to the specifit value for BaseInfo section.
        @note: there are not to check the value is valid or not, so need
               to ensure value is valid before invoke this method.
        """
        self.cp.set('BaseInfo', option, value)
            
    def getOptions(self, section):
        ret = []
        opts = self.cp.options(section)
        for item in opts:
            ret.append(self.cp.get(section, item))
        return ret

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
        if not self.cp.has_section(section):
            EH.valueError('No Section Error: {0}'.format(section))
        
        opts = self.cp.options(section)
        if str(num) not in opts:
            EH.valueError('{0} is not in the options'.format(num))
        return self.cp.get(section, num)

    def type2num(self, section, Type):
        """Transform the Type to correctly maped Number.
        """
        if not self.cp.has_section(section):
            EH.valueError('No Section Error: {0}'.format(section))
        
        opts = self.cp.options(section)
        for item in opts:
            if Type == self.cp.get(section, item):
                return int(item)
        else:
            EH.valueError('{0} is not a valid type.'.format(consuType))


if __name__ == '__main__':
    cm = ConfigManip()
#    for item in cm.getConsumingType():
#        print item,
    print '\n\n'
#    for item in cm.getPaymentType():
#        print item,
    print cm.num2type('ConsumingType', '5')
    print cm.type2num('ConsumingType', '食物')
    print cm.num2type('PaymentType', '2')
    print cm.type2num('PaymentType', '现金')
    print cm.num2type('ConsumingCatagory', '0')
    print cm.type2num('ConsumingCatagory', '商务')
    
    
