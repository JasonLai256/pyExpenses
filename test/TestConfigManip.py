#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys
import os
import copy

try:
    from ConfigManip import Config, _exportObj
except ImportError:
    sys.path.append(os.path.abspath('..'))
    from ConfigManip import Config, _exportObj
from RecManipImpl import BaseRecord


class TestConfigManip(unittest.TestCase):
    
    def setUp(self):
        self.obj = copy.deepcopy(Config.obj)

    def tearDown(self):
        _exportObj(self.obj, path=os.path.abspath('.'))

    def test_getInfos(self):
        item = Config.getInfos('version')
        self.assertEqual(
            Config.obj['BaseInfo']['version'],
            item
        )

    def test_setInfo(self):
        Config.setInfo('language', u'en')
        self.assertNotEqual(
            self.obj['BaseInfo']['language'],
            Config.obj['BaseInfo']['language']
        )

    def test_getOptions(self):
        seq = Config.getOptions('Type')
        mtypes = [item[0] for item in seq]
        self.assertListEqual(
            Config.obj['Type']['type_order'],
            mtypes
        )

    def test_addOptions(self):
        Config.addOption('Tag', u'+1')
        self.assertTrue('+1' in Config.obj['Tag']['types'])
#        Config.addOption('Type', (u'礼物', u'Mac Mini'))
#        assertTrue((u'礼物', u'Mac Mini') in )

    def test_delOptions(self):
        Config.delOption('Currency', u'$')
        self.assertTrue('$' not in Config.obj['Currency']['types'])
        Config.addOption('Currency', u'$')
#        Config.delOption('Type', (u'休闲娱乐', u'聚会'))
#        assertTrue((u'休闲娱乐', u'聚会') not in )

    def test_getDefaults(self):
        d = Config.getDefaults()
        self.assertEqual(Config.obj['Type']['default'], d[0])
        self.assertEqual(Config.obj['Payment']['default'], d[1])
        self.assertEqual(Config.obj['Currency']['default'], d[2])
        self.assertEqual(Config.obj['Tag']['default'], d[3])

    def test_setDefault(self):
        rec = BaseRecord(1, (u'食品酒水', u'水果零食'), u'现金', u'￥')
        Config.setDefault(rec)

        self.assertEqual(Config.obj['Type']['default'], rec.type)
        self.assertEqual(Config.obj['Payment']['default'], rec.payment)
        self.assertEqual(Config.obj['Currency']['default'], rec.currency)
        self.assertEqual(Config.obj['Tag']['default'], rec.tag)

        # the first item of 'types' should be the default type.
        self.assertEqual(Config.obj['Type']['type_order'][0], rec.type[0])
        self.assertEqual(Config.obj['Payment']['types'][0], rec.payment)
        self.assertEqual(Config.obj['Currency']['types'][0], rec.currency)
        self.assertEqual(Config.obj['Tag']['types'][0], rec.tag)


if __name__ == '__main__':
    unittest.main()
