#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys
import os
from datetime import date

try:
    from pyExpenses.Projects import ConsumingProject
except ImportError:
    sys.path.append(os.path.abspath('..'))
    from pyExpenses.Projects import ConsumingProject
from TestRecManip import TEST_SAMPS


class TestConsumingProject(unittest.TestCase):

    def test_import_export_dict(self):
        proj = ConsumingProject(999, date(2012, 1, 1), 303)
        
        dates = date(2012, 1, 1), date(2012, 1, 3)
        for d in dates:
            for rec in TEST_SAMPS[d]:
                proj.register(d, rec)

        tdict = proj.export_to_dict()
        proj2 = ConsumingProject()
        proj2.import_from_dict(tdict)

        self.assertEqual(proj.p_start_time, proj2.p_start_time)
        self.assertEqual(proj.p_accumt_amount, proj2.p_accumt_amount)
        self.assertEqual(proj.p_recs_amount, proj2.p_recs_amount)
        self.assertListEqual(proj.p_progress_info, proj2.p_progress_info)

        self.assertEqual(proj.p_accumt_amount, 103.0)
        self.assertEqual(proj.p_recs_amount, 4)

        tdict2 = proj2.export_to_dict()
        self.assertDictEqual(tdict, tdict2)

    def test_report(self):
        pass

    def test_recursion(self):
        pass

    def test_project(self):
        pass
        
if __name__ == '__main__':
    unittest.main()
