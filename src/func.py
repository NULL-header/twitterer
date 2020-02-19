from logging import getLogger, NullHandler
import pickle
import os

logger = getLogger("core")
logger.addHandler(NullHandler())


class Core(object):
    def __init__(self):
        self.__binded_channel = {}
        self.__savepath = ""

    def load_savedata(self):
        if os.path.exists(self.__savepath):
            try:
                with open(self.__savepath, "rb")as f:
                    self.__binded_channel = pickle.load(f)
                    logger.debug("load data {0}".format(self.__binded_channel))
                    return True
            except Exception:
                logger.debug("data do not exist.")
        return False

    def bind(self, channel_id):
        if self.__binded_channel.get(channel_id):
            return False
        self.__binded_channel[channel_id] = {
            "id": None,
            "slug": None,
            "twitterer": None,
        }
        with open(self.__savepath, "wb")as f:
            pickle.dump(self.__binded_channel, f)
        logger.debug("check {0}".format(self.__binded_channel))
        return True

    def checker(self, id):
        return id in self.__binded_channel.keys()

    def clean(self):
        self.__binded_channel = {}
        if os.path.exists(self.__savepath):
            os.remove(self.__savepath)
            return True
        return False

    @property
    def binded_channel(self):
        return self.__binded_channel

    def setter(self, *, path):
        self.__savepath = path
