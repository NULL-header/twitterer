# coding:utf-8

import os
import unittest

import app


class AppTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        f = open('test.txt', 'w')
        f.writelines('test:whips')
        # 初期化処理
        pass

    @classmethod
    def tearDown(self):
        os.remove('test.txt')
        # 終了処理
        pass

    def test_read_key_normal(self):
        self.assertEqual({'test': 'whips'}, app.read_keys('test.txt'))

    def test_read_key_ellegal(self):
        self.assertNotEqual({'test': 'whps'}, app.read_keys('test.txt'))


if __name__ == "__main__":
    unittest.main()
