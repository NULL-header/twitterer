# encoding:utf-8
import sys
from logging import DEBUG, FileHandler, Formatter, StreamHandler, getLogger

logger = getLogger("main")
handler = StreamHandler()
fhandler = FileHandler(filename="..\\.data\\app.log",
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
dhandler = FileHandler(filename="..\\.data\\discord.log",
                       encoding="utf-8", mode="w")
dhandler.setLevel(DEBUG)
dhandler.setFormatter(formatter)
dlogger.addHandler(dhandler)
blogger = getLogger("bot")
blogger.setLevel(DEBUG)
blogger.addHandler(handler)
bhandler = FileHandler(filename="..\\.data\\bot.log",
                       encoding="utf-8", mode="w")
blogger.addHandler(bhandler)

logger.debug("set up.")


def read_keys(path: str) -> dict:
    '''
    this function is only to read token.
    if key.txt does not exist, log show FileNotFoundError and Type Error.
    '''
    logger.debug("read_keys funciton is called.")
    try:
        logger.debug("read key.txt.")
        with open(path, "r")as f:
            text = f.readlines()
            list_dict = []
            for t in text:
                list_dict.append(tuple(t.split(":")))
            return dict(list_dict)
    except Exception:
        logger.error("could not read key.txt;\n\n"
                     "with this traceback:{0}\n".format(sys.exc_info()))
        logger.error("put key.txt.")
        return None
    finally:
        logger.debug("read_keys finished.")


def main():
    logger.debug("main wake.")
    from bot import Bot
    bot = Bot()
    try:
        TOKEN = read_keys("..\\.data\\key.txt")["token"]
        logger.debug("bot run.")
        bot.run(TOKEN)
    except Exception:
        logger.error("could not read token;\n\n"
                     "with this traceback:{0}\n".format(sys.exc_info()))
    finally:
        logger.debug("main function finished.")


if __name__ == "__main__":
    logger.debug("Start main function.")
    main()
