import unittest
import os
import pickle
from src.func import Core
from src import setting
from logging import getLogger, StreamHandler, DEBUG, Formatter


class TestCore(unittest.TestCase):
    def setUp(self):
        self.path = "testsavedata.txt"
        self.c = Core()
        self.batch = {
            "path": self.path,
            "Ck": setting.CONSUMER_KEY,
            "Cs": setting.CONSUMER_SERCRET,
            "At": setting.ACCESS_TOKEN,
            "As": setting.ACCESS_TOKEN_SERCRET,
        }
        self.c.setter(**self.batch)

    def test_init(self):
        self.assertEquals(self.c.binded_channel, {})

        self.setuper_init()
        core = Core()
        core.setter(path=self.testdata_init)
        core.load_savedata()
        self.assertEquals(core.binded_channel, self.moc_init)
        self.setdowner_init()

    def setuper_init(self):
        self.testdata_init = "testdata_init.txt"
        self.moc_init = {
            111: None
        }
        with open(self.testdata_init, "wb")as f:
            pickle.dump(self.moc_init, f)

    def setdowner_init(self):
        os.remove(self.testdata_init)

    def test_load_savedata(self):
        core = Core()
        flag = core.load_savedata()
        self.assertFalse(flag)

        self.setuper_load_savedata()
        core.setter(path=self.testdata_load_savedata)
        flag = core.load_savedata()
        self.assertTrue(flag)
        self.setdowner_load_savedata()

    def setuper_load_savedata(self):
        self.testdata_load_savedata = "testdata_load_savedata.txt"
        self.moc_load_savedata = {
            222: None
        }
        with open(self.testdata_load_savedata, "wb")as f:
            pickle.dump(self.moc_load_savedata, f)

    def setdowner_load_savedata(self):
        os.remove(self.testdata_load_savedata)

    def test_bind(self):
        flag = self.c.bind(100)
        self.assertTrue(100 in self.c.binded_channel)
        self.assertEquals(flag, True)
        result = os.path.exists(self.path)
        self.assertEquals(result, True)

        flag = self.c.bind(100)
        self.assertEquals(flag, False)

    def test_checker(self):
        self.c.bind(100)
        self.assertTrue(self.c.checker(100))

    def test_clean(self):
        self.c.bind(100)
        flag = self.c.clean()
        self.assertEquals(self.c.binded_channel, {})
        self.assertTrue(flag)
        flag = flag = self.c.clean()
        self.assertFalse(flag)

    def test_set_id(self):
        flag = self.c.set_id(100, "aaa")
        self.assertFalse(flag)
        self.c.bind(100)
        flag = self.c.set_id(100, "aaa")
        self.assertTrue(flag)
        self.assertEquals(self.c.binded_channel[100].twid, "aaa")
        flag = self.c.set_id(100, "@bbb")
        self.assertTrue(flag)
        self.assertEquals(self.c.binded_channel[100].twid, "bbb")

    def test_set_list(self):
        flag = self.c.set_list(100, "aaa")
        self.assertFalse(flag)
        self.c.bind(100)
        flag = self.c.set_list(100, "aaa")
        self.assertTrue(flag)
        self.assertEquals(self.c.binded_channel[100].slug, "aaa")

    def test_(self):
        pass

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)


class loggercheck(TestCore):
    logger = getLogger("core")
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    formatter = Formatter(
        "\n%(relativeCreated)6d:[%(asctime)s][%(name)10s][%(levelname)s]:"
        "%(message)s\n")
    handler.setFormatter(formatter)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)


if __name__ == "__main__":
    unittest.main()
