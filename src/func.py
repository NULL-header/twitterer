from logging import getLogger, NullHandler

logger = getLogger("core")
logger.addHandler(NullHandler())


class Core(object):
    def __init__(self):
        self.__binded_channel = []

    def setter(self, channel_id):
        self.__binded_channel.append(channel_id)
        logger.debug("check {0}".format(self.__binded_channel))

    def checker(self, id):
        return id in self.__binded_channel

    @property
    def binded_channel(self):
        return self.__binded_channel
