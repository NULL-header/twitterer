# encoding:utf-8
import sys
from logging import DEBUG, FileHandler, Formatter, StreamHandler, getLogger
import setting

logger = getLogger("main")
handler = StreamHandler()
fhandler = FileHandler(filename=".data/app.log",
                       encoding="utf-8", mode="w")
handler.setLevel(DEBUG)
formatter = Formatter(
    "%(relativeCreated)6d:[%(asctime)s][%(name)10s][%(levelname)s]:"
    "%(message)s")
handler.setFormatter(formatter)
logger.setLevel(DEBUG)
logger.addHandler(handler)
dlogger = getLogger("discord")
dlogger.setLevel(DEBUG)
dhandler = FileHandler(filename=".data/discord.log",
                       encoding="utf-8", mode="w")
dhandler.setLevel(DEBUG)
dhandler.setFormatter(formatter)
dlogger.addHandler(dhandler)
blogger = getLogger("bot")
blogger.setLevel(DEBUG)
blogger.addHandler(handler)
bhandler = FileHandler(filename=".data/bot.log",
                       encoding="utf-8", mode="w")
blogger.addHandler(bhandler)
bindlogger = getLogger("core")
bindlogger.setLevel(DEBUG)
bindlogger.addHandler(handler)
twilogger = getLogger("twitter")
twilogger.setLevel(DEBUG)
twilogger.addHandler(handler)


logger.debug("set up.")


def keys():
    return {
        "DISCORD_TOKEN": setting.DISCORD_TOKEN,
        "DISCORD_WEBHOOK": setting.DISCORD_WEBHOOK,
        "CONSUMER_KEY": setting.CONSUMER_KEY,
        "CONSUMER_SERCRET": setting.CONSUMER_SERCRET,
        "ACCESS_TOKEN": setting.ACCESS_TOKEN,
        "ACCESS_TOKEN_SERCRET": setting.ACCESS_TOKEN_SERCRET,
    }


def main():
    args = sys.argv
    if len(args) == 1:
        logger.debug("args have no items.")
        prfix = "!DEFAULT!"
    else:
        logger.debug("args have items, {}.".format(args[1]))
        prfix = args[1]
    try:
        from bot import Bot
        bot = Bot(keys(), prfix=prfix)
        logger.debug("bot run.")
        bot.wake()
    except Exception:
        logger.error("could not read token;\n\n"
                     "with this traceback:{0}\n".format(sys.exc_info()))


if __name__ == "__main__":
    main()
