from logging import getLogger, NullHandler
import pickle
import os
from src.datasome import DataofCore

logger = getLogger("core")
logger.addHandler(NullHandler())


class Core(object):
    def __init__(self):
        self.__binded_channel = {}
        self.data = {
            "path": "",
            "CK": None,
            "CS": None,
            "AT": None,
            "AS": None,
        }

    def load_savedata(self):
        if os.path.exists(self.data["path"]):
            try:
                with open(self.data["path"], "rb")as f:
                    self.__binded_channel = pickle.load(f)
                    logger.debug("load data {0}".format(self.__binded_channel))
                    return True
            except Exception:
                logger.debug("data do not exist.")
        return False

    def bind(self, channel_id):
        if self.__binded_channel.get(channel_id):
            return False
        self.__binded_channel[channel_id] = DataofCore()
        with open(self.data["path"], "wb")as f:
            pickle.dump(self.__binded_channel, f)
        logger.debug("check {0}".format(self.__binded_channel))
        return True

    def checker(self, id):
        return id in self.__binded_channel.keys()

    def clean(self):
        self.__binded_channel = {}
        if os.path.exists(self.data["path"]):
            os.remove(self.data["path"])
            return True
        return False

    def setter(self, *, path=None, Ck=None, Cs=None, At=None, As=None):
        datadict = {
            path: "path",
            Ck: "CK",
            Cs: "CS",
            At: "AT",
            As: "AS",
        }
        for i in datadict.keys():
            if i:
                self.data[datadict[i]] = i

    def set_id(self, channel, id_):
        bindeddata = self.__binded_channel.get(channel)
        if bindeddata:
            bindeddata.twid = id_
            logger.debug("id seted {0}".format(id))
            return True
        return False

    @property
    def binded_channel(self):
        return self.__binded_channel
