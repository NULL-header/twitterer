from logging import getLogger, NullHandler

logger = getLogger("core")
logger.addHandler(NullHandler())


class Core(object):
    def __init__(self):
        self.binded_channel = []

    def setter(self, channel_id):
        self.binded_channel.append(channel_id)
        logger.debug("check {0}".format(self.binded_channel))

    def checker(self, id):
        return (id in self.binded_channel)
