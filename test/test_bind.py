# coding:utf-8
import os
import pickle
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..\\doc'))

try:
    from bind import Bind
    from twitterer import Mytwitterer
finally:
    pass


class TestBind1(unittest.TestCase):
    def setUp(self):
        with open("..\\.data\\key.txt", "r")as f:
            text = f.readlines()
            list_dict = []
            for t in text:
                list_dict.append(tuple(t.rstrip().split(":")))
        ld = dict(list_dict)
        self.path_data = "testdata.pickle"
        self.path_err = "..\\.data\\errcode.txt"
        d = {
            "pd": self.path_data,
            "pe": self.path_err,
            "ck": ld["CK"],
            "cs": ld["CS"],
            "at": ld["AT"],
            "as": ld["AS"],
        }
        self.d = d
        self.b = Bind()
        result = self.b.setter(d)
        self.assertEqual(100, result)
        result = self.b.read_data(self.path_data, self.path_err)
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
                    "tw": Mytwitterer(self.d["ck"], self.d["cs"],
                                      self.d["at"], self.d["as"]),
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

    def test_clean_bind(self):
        with open(self.path_data, "w")as f:
            f.write("a")
        result = self.b.clean_bind()
        self.assertEqual(100, result)
        result = self.b.clean_bind()
        self.assertEqual(305, result)

    def test_set_id(self):
        self.b.set_bind(1, 2)
        result = self.b.set_id(1, 2, "aaaa")
        self.assertEqual(result, 100)
        self.assertEqual(self.b.data[1][2]["id"], "aaaa")
        self.b.set_id(1, 2, "@aaa")
        self.assertEqual(self.b.data[1][2]["id"], "aaa")
        result = self.b.set_id(1, 2, None)
        self.assertEqual(result, 306)

    def test_setter(self):
        data_dict = {
            "pd": "a",
            "pe": "b",
            "ck": "c",
            "cs": "d",
            "at": "e",
            "as": "f",
        }
        self.assertEqual(self.b.setter(data_dict), 100)
        self.assertEqual(self.b.path_data, "a")
        self.assertEqual(self.b.path_err, "b")
        self.assertEqual(self.b.CK, "c")
        self.assertEqual(self.b.CS, "d")
        self.assertEqual(self.b.AT, "e")
        self.assertEqual(self.b.AS, "f")

    def test_(self):
        pass

    def test_(self):
        pass

    def tearDown(self):
        try:
            os.remove(self.path_data)
        except Exception:
            pass


class TestBind2(unittest.TestCase):

    def setUp(self):
        self.b = Bind()
        self.path_data = "testdata.pickle"
        self.path_err = "..\\.data\\errcode.txt"
        result = self.b.read_data(self.path_data, self.path_err)
        self.assertEqual(result, 302)

    def test_(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
