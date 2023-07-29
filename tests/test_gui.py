import unittest
import numpy as np
import os
import cv2
import logging
from gui.__main__ import USize

class GuiTestCase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s', level = logging.DEBUG)

    def test_base(self):
        self.assertEqual(1,1)

    def test_uszie(self):
        size = USize(0.25, USize.Unit.MB)
        self.assertEqual(int(size), int(0.25*1024*1024))
        self.assertEqual(str(size), '256.0 KB')
        self.assertEqual(size.unit, USize.Unit.MB)