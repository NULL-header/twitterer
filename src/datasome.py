from os import path as ospath
from sys import path as syspath

try:
    # These lines are for unittest.
    syspath.append(ospath.join(ospath.dirname(__file__), '..'))
    from src.twitter import MyTwitter
except Exception:
    pass


class DataofCore(object):
    def __init__(self, *, Ck=None, Cs=None, At=None, As=None):
        self.__id = None
        self.__slug = None
        self.__twitter = None
        if Ck and Cs and At and As:
            try:
                self.__twitter = MyTwitter(Ck, Cs, At, As)
            except Exception:
                pass

    @property
    def twid(self):
        return self.__twid

    @twid.setter
    def twid(self, item):
        self.__twid = item

    @property
    def slug(self):
        return self.__slug

    @slug.setter
    def slug(self, item):
        self.__slug = item

    @property
    def twitter(self):
        return self.__twitter

    @twitter.setter
    def twitter(self, item):
        self.__twitter = item
