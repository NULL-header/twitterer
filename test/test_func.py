import unittest
import os
import pickle
from src.func import Core
from logging import getLogger, StreamHandler, DEBUG, Formatter


class TestCore(unittest.TestCase):
    def setUp(self):
        self.path = "testsavedata.txt"
        self.c = Core(self.path)

    def test_init(self):
        self.assertEquals(self.c.binded_channel, {})

        self.setuper_init()
        core = Core(self.testdata_init)
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
        self.assertEquals(flag, True)

    def test_setpath(self):
        self.c.setpath()
        self.assertTrue(True)

    def test_(self):
        pass

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)


class loggercheck(TestCore):
    def setUp(self):
        logger = getLogger("core")
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        formatter = Formatter(
            "%(relativeCreated)6d:[%(asctime)s][%(name)10s][%(levelname)s]:"
            "%(message)s")
        handler.setFormatter(formatter)
        logger.setLevel(DEBUG)
        logger.addHandler(handler)
        super().setUp()
