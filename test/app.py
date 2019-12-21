# encoding:utf-8
from logging import DEBUG, FileHandler, Formatter, StreamHandler, getLogger

logger = getLogger("main")
handler = StreamHandler()
handler.setLevel(DEBUG)
formatter = Formatter(
    "%(relativeCreated)6d:[%(asctime)s][%(name)10s][%(levelname)s]:"
    "%(message)s")
handler.setFormatter(formatter)
logger.setLevel(DEBUG)
logger.addHandler(handler)
dlogger = getLogger("discord")
dlogger.setLevel(DEBUG)
dhandler = FileHandler(filename="..\\.data\\discord.log",
                       encoding="utf-8", mode="w")
dhandler.setLevel(DEBUG)
dhandler.setFormatter(formatter)
dlogger.addHandler(dhandler)

logger.debug("set up.")


def main():
    logger.debug("main wake.")
    from bot import Bot
    bot = Bot()
    logger.debug("bot run.")
    bot.run()


if __name__ == "__main__":
    logger.debug("Start main function.")
    main()
