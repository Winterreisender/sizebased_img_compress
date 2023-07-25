import unittest
from sizebased_img_compress.smart_compress import smart_compress, loss_compress
import numpy as np
from functools import lru_cache
import os
import cv2
import logging

class MainTestCase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s', level = logging.DEBUG)


    def check_result(self, img, new_img_bytes, target_size, quality):
        print(f"result={len(new_img_bytes)}, target={target_size}, quality={quality}")
        assert len(new_img_bytes) <= target_size
        assert quality+3>100 or len(loss_compress(img, quality+3)) >= target_size

    @lru_cache(1)
    def get_img(self):
        original_size = os.path.getsize('./tests/example.jpg')
        print(original_size)

        img_bytes = None
        with open('./tests/example.jpg', 'rb') as f:
            img_bytes = f.read()

        img = cv2.imdecode(np.asarray(bytearray(img_bytes), dtype='uint8'), cv2.IMREAD_UNCHANGED)
        return (img, original_size)

    def test_base(self):
        self.assertEqual(1,1)

    def test_common(self):
        img, origial_size = self.get_img()
        for target_size_mb in np.linspace(0.6,1.4,10):
            target_size = int(target_size_mb*1024*1024)
            quality,new_img_bytes = smart_compress(img, target_size)
            self.check_result(img, new_img_bytes, target_size, quality)


    @unittest.expectedFailure
    def test_extreme(self):
        img, origial_size = self.get_img()
        for target_size in [0]:
            quality,new_img_bytes = smart_compress(img, target_size)
            self.check_result(img, new_img_bytes, target_size, quality)

    def test_special(self):
        img, origial_size = self.get_img()
        for target_size in [len(loss_compress(img, x)) for x in range(5,101,5)]:
            quality,new_img_bytes = smart_compress(img, target_size)
            self.check_result(img, new_img_bytes, target_size, quality)
