# coding:utf-8
import os
import pickle
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

    def test_read_data(self):
        result = self.b.read_data("a", "b")
        self.assertEqual(result, 201)
        path_err = "testcase_read_data_err.txt"
        path_data = "testcase_read_data_data.pickle"
        with open(path_err, "w")as f:
            text = "0:done"
            f.write(text)
        with open(path_data, "wb")as f:
            pickle.dump({1: None}, f)
        result = self.b.read_data("a", path_err)
        self.assertEqual(result, 302)
        result = self.b.read_data(path_data, path_err)
        self.assertEqual(result, 100)
        self.assertTrue(bool(self.b.data))
        os.remove(path_err)
        os.remove(path_data)

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

    def test_check_bind(self):
        gid = 111
        cid = 222
        self.b.set_bind(gid, cid)
        self.assertEqual(self.b.check_bind(gid, cid), [True, 100])
        self.assertEqual(self.b.check_bind(1, cid), [False, 303])
        self.assertEqual(self.b.check_bind(gid, 1), [False, 304])

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
