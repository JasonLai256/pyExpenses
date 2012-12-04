import TestRecParser
import unittest

def suite():
    return unittest.TestLoader().discover(start_dir='.', pattern='Test*.py')
