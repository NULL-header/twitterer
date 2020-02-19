from logging import getLogger, NullHandler
import pickle
import os

logger = getLogger("core")
logger.addHandler(NullHandler())


class Core(object):
    def __init__(self, path):
        self.__binded_channel = {}
        self.__savepath = path
        if os.path.exists(path):
            try:
                with open(path, "rb")as f:
                    self.__binded_channel = pickle.load(f)
                    logger.debug("load data {0}".format(self.__binded_channel))
            except Exception:
                logger.debug("can not load data")

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
        return True

    def setpath(self):
        pass

    @property
    def binded_channel(self):
        return self.__binded_channel

    def load_data(self):
        pass
