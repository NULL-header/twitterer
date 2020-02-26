from logging import getLogger, NullHandler
import pickle
import os
import sys
import asyncio
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
        self.stock = {}

    def saver(self):
        with open(self.data["path"], "wb")as f:
            pickle.dump(self.__binded_channel, f)

    def load_savedata(self):
        # You should use this after using of self.setter function.
        if os.path.exists(self.data["path"]):
            try:
                with open(self.data["path"], "rb")as f:
                    self.__binded_channel = pickle.load(f)
                    logger.debug("load data {0}".format(self.__binded_channel))
                    return True
            except Exception:
                logger.debug("[load_savedata]data do not exist.")
        return False

    def bind(self, channel_id):
        # this method writes some data objects
        #  to internal dictionary variable object.
        if self.__binded_channel.get(channel_id):
            return False
        items = [
            self.data["CK"],
            self.data["CS"],
            self.data["AT"],
            self.data["AS"],
        ]
        self.__binded_channel[channel_id] = DataofCore(*items)
        self.saver()
        logger.debug("[bind]check {0}".format(self.__binded_channel))
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
            logger.debug("[clean]done Successfully.")
            return True
            logger.debug("[clean]done without deleting savedata file.")
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
        if id_.startswith("@"):
            id_ = id_[1:]
        if bindeddata:
            bindeddata.twid = id_
            logger.debug("[set_id]id seted {0}".format(id_))
            self.saver()
            return True
        return False

    def catch_lists(self, channel):
        # It can not be written test because of using Twitter API.
        bindeddata = self.__binded_channel.get(channel)
        if bindeddata:
            flag = bindeddata.listlist()
            if flag:
                return flag
        return False

    def set_list(self, channel, slug):
        # TODO:delete it's redundancy with set_id function.
        bindeddata = self.__binded_channel.get(channel)
        if bindeddata:
            bindeddata.slug = slug
            self.saver()
            logger.debug("[set_list]slug seted {0}".format(slug))
            return True
        return False

    async def stock_tweet(self, channel, pathdir=".data"):
        # It use Twitter API, but it does not use the api if
        #  self.stock[channel]'s length is bigger than 200; So it can be
        #  written test when it is bigger.
        if not self.stock.get(channel):
            self.stock[channel] = []
        while len(self.stock[channel]) < 200:
            logger.debug("Adding tweets into stock.")
            self.stock[channel].extend(
                self.__binded_channel[channel].catch_tweet())
            asyncio.sleep(60)
        savetweets = []
        for i in range(100):
            savetweets.append(self.stock[channel].pop(0))

    @property
    def binded_channel(self):
        return self.__binded_channel
