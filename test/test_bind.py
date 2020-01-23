# coding:utf-8
import logging
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
        with open(".data\\key.txt", "r")as f:
            text = f.readlines()
            list_dict = []
            for t in text:
                list_dict.append(tuple(t.rstrip().split(":")))
        ld = dict(list_dict)
        self.path_data = "testdata.pickle"
        d = {
            "pd": self.path_data,
            "ck": ld["CK"],
            "cs": ld["CS"],
            "at": ld["AT"],
            "as": ld["AS"],
        }
        self.d = d
        self.b = Bind()
        self.b.setter(d)
        self.assertEqual(self.b.path_data, d["pd"])
        self.assertEqual(self.b.CK, d["ck"])
        self.assertEqual(self.b.CS, d["cs"])
        self.assertEqual(self.b.AT, d["at"])
        self.assertEqual(self.b.AS, d["as"])
        self.b.read_data()
        self.assertEqual(self.b.data, {})

    def test_read_data(self):
        d_test = {
            "pd": "a",
            "ck": self.d["ck"],
            "cs": self.d["cs"],
            "at": self.d["at"],
            "as": self.d["as"],
        }
        path_data = "testcase_read_data_data.pickle"
        with open(path_data, "wb")as f:
            pickle.dump({1: None}, f)
        self.b.setter(d_test)
        self.b.read_data()
        self.assertFalse(bool(self.b.data))
        d_test["pd"] = path_data
        self.b.setter(d_test)
        self.b.read_data()
        self.assertTrue(bool(self.b.data))
        os.remove(path_data)

    def test_new(self):
        b = Bind()
        self.assertEqual({}, b.data)

    def test_set_bind(self):
        gid = 11111111
        cid = 22222222
        self.b.set_bind(gid, cid)
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
        self.assertEqual(self.b.data, testcase)
        self.assertEqual(self.b.set_bind(gid, cid), None)

    def test_check_bind(self):
        gid = 111
        cid = 222
        self.b.set_bind(gid, cid)
        self.assertEqual(self.b.check_bind(gid, cid), True)
        self.assertEqual(self.b.check_bind(1, cid), False)
        self.assertEqual(self.b.check_bind(gid, 1), False)

    def test_clean_bind(self):
        with open(self.path_data, "w")as f:
            f.write("a")
        self.b.clean_bind()
        self.assertEqual({}, self.b.data)

    def test_set_id(self):
        self.b.set_bind(1, 2)
        self.b.set_id(1, 2, "aaaa")
        self.assertEqual(self.b.data[1][2]["id"], "aaaa")
        self.b.set_id(1, 2, "@aaa")
        self.assertEqual(self.b.data[1][2]["id"], "aaa")

    def test_setter(self):
        data_dict = {
            "pd": "a",
            "ck": "c",
            "cs": "d",
            "at": "e",
            "as": "f",
        }
        self.b.setter(data_dict)
        self.assertEqual(self.b.path_data, "a")
        self.assertEqual(self.b.CK, "c")
        self.assertEqual(self.b.CS, "d")
        self.assertEqual(self.b.AT, "e")
        self.assertEqual(self.b.AS, "f")

    def test_set_list(self):
        self.b.set_bind(1, 2)
        self.b.set_list(1, 2, "b")
        self.b.set_id(1, 2, "a")
        self.assertEqual("a", self.b.data[1][2]["id"])
        self.b.set_list(1, 2, "b")
        self.assertEqual("b", self.b.data[1][2]["slug"])

    def test_(self):
        pass

    def tearDown(self):
        try:
            os.remove(self.path_data)
        except Exception:
            pass


class TestBindsLogger(TestBind1):
    def setUp(self):
        logger = logging.getLogger("bind")
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(relativeCreated)6d:[%(asctime)s]"
            "[%(name)10s][%(levelname)s]:%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        super().setUp()


if __name__ == "__main__":
    unittest.main()
