import unittest
from src.func import Core


class TestCore(unittest.TestCase):
    def setUp(self):
        self.c = Core()

    def test_init(self):
        self.assertEquals(self.c.binded_channel, [])

    def test_setter(self):
        self.c.setter(100)
        self.assertTrue(100 in self.c.binded_channel)

    def test_checker(self):
        self.c.setter(100)
        self.assertTrue(self.c.checker(100))

    def test_(self):
        pass
