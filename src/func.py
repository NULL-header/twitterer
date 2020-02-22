from logging import getLogger, NullHandler
import pickle
import os
import sys

try:
    # These lines are for unittest.
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from src.datasome import DataofCore
except Exception:
    pass

logger = getLogger("core")
logger.addHandler(NullHandler())


class Core(object):
    # it has data object as DataofCore, and this is singleton.
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
        # You should use this after using of self.setter function.
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
        # this method writes some data objects
        #  to internal dictionary variable object.
        if self.__binded_channel.get(channel_id):
            return False
        self.__binded_channel[channel_id] = DataofCore()
        with open(self.data["path"], "wb")as f:
            pickle.dump(self.__binded_channel, f)
        logger.debug("check {0}".format(self.__binded_channel))
        return True

    def checker(self, id):
        # This function should be used at outer of this class,
        #  for example, this function can be useful
        #  on conditional expression of if sentence.
        return id in self.__binded_channel.keys()

    def clean(self):
        self.__binded_channel = {}
        if os.path.exists(self.data["path"]):
            os.remove(self.data["path"])
            return True
        return False

    def setter(self, *, path=None, Ck=None, Cs=None, At=None, As=None):
        # This method can be use with 5 arguments, and with only path argument.
        # The path argment is used on saving pickle and deleting it.
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
        # this function writes some data into DataofCore of data object.
        bindeddata = self.__binded_channel.get(channel)
        if bindeddata:
            bindeddata.twid = id_
            logger.debug("id seted {0}".format(id))
            return True
        return False

    @property
    def binded_channel(self):
        return self.__binded_channel
