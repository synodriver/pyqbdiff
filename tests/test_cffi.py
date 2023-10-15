"""
Copyright (c) 2008-2023 synodriver <diguohuangjiajinweijun@gmail.com>
"""
import os

os.environ["QBDIFF_USE_CFFI"] = "1"
from unittest import TestCase

from qbdiff import compute, error, patch, version, QBERR_OK


class Testcy(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_version(self):
        print(version())
        self.assertTrue(isinstance(version(), str))

    def test_error(self):
        print(error(1))
        self.assertTrue(isinstance(error(1), str))

    def test_compute(self):
        old = b"1234"
        new_ = b"123456"
        compute(old, new_, "diff_tmp.bin")
        with open("diff_tmp.bin", "rb") as f:
            diff = f.read()
        patch(old, diff, "new.bin")
        with open("new.bin", "rb") as f:
            newf = f.read()
        self.assertEquals(new_, newf, "patch fail")


if __name__ == "__main__":
    import unittest

    unittest.main()
