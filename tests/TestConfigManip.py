#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys
import os
import copy

from pyExpenses.ConfigManip import Config, _exportObj
from pyExpenses.Record import BaseRecord


class TestConfigManip(unittest.TestCase):
    
    def setUp(self):
        self.obj = copy.deepcopy(Config.obj)

    def tearDown(self):
        _exportObj(self.obj, Config.objfile)

    def test_getInfo(self):
        item = Config.getInfo('version')
        self.assertEqual(
            Config.obj['BaseInfo']['version'],
            item
        )

    def test_setInfo(self):
        Config.setInfo('language', u'cn')
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
#        Config.addOption('Type', (u'Gift', u'Mac Mini'))
#        assertTrue((u'Gift', u'Mac Mini') in )

    def test_delOptions(self):
        Config.delOption('Currency', u'USD')
        self.assertTrue('USD' not in Config.obj['Currency']['types'])
        Config.addOption('Currency', u'USD')
#        Config.delOption('Type', (u'Recreation', u'Party'))
#        assertTrue((u'Recreation', u'Party') not in )

    def test_getDefaults(self):
        d = Config.getDefaults()
        self.assertEqual(Config.obj['Type']['default'], d[0])
        self.assertEqual(Config.obj['Payment']['default'], d[1])
        self.assertEqual(Config.obj['Currency']['default'], d[2])
        self.assertEqual(Config.obj['Tag']['default'], d[3])

    def test_setDefault(self):
        rec = BaseRecord(1, (u'Food & Drinks', u'Snacks'), u'Cash', u'CHY')
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

    def test_getBufferObj_and_setBufferObj(self):
        projbuf = {
            'python': 6,
            'tcl': 3,
            'ruby': 4,
            'lua': 3,
            'perl': 4,
        }
        Config.setProjectBuffer(projbuf)
        bufobj = Config.getProjectBuffer()
        self.assertDictEqual(bufobj, projbuf)
        Config.setProjectBuffer({})

        rec = BaseRecord(1, (u'Food & Drinks', u'Snacks'), u'Cash', u'CHY')
        recbuf = [
            [
                '2012-01-03',
                rec.amount,
                rec.type[0],
                rec.type[1],
                rec.payment,
                rec.currency,
                rec.tag,
                rec.comment
            ]
        ]
        Config.setRecordBuffer(recbuf)
        bufobj = Config.getRecordBuffer()
        self.assertListEqual(bufobj, recbuf)
        Config.setRecordBuffer([])
