# coding:utf-8
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..\\doc'))

try:
    from bind import Bind
finally:
    pass


class TestBind1(unittest.TestCase):
    def setUp(self):
        self.b = Bind()
        result = self.b.read_data("..\\.data\\aa", "..\\.data\\errcode.txt")
        self.assertEqual(result, 302)

    def test_new(self):
        b = Bind()
        self.assertEqual({}, b.data)

    def test_set_bind(self):
        gid = 11111111
        cid = 22222222
        result = self.b.set_bind(gid, cid)
        testcase = {
            gid: {
                cid: {
                    "tw": None,
                    "id": None,
                    "slug": None
                }
            }
        }
        self.assertEqual(result, 100)
        self.assertEqual(self.b.data, testcase)
        self.assertEqual(self.b.set_bind(gid, cid), 301)

    def test_(self):
        pass

    def test_(self):
        pass

    def test_(self):
        pass

    def tearDown(self):
        pass


class TestBind2(unittest.TestCase):

    def setUp(self):
        pass

    def test_(self):
        pass

    def test_(self):
        pass

    def test_(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
