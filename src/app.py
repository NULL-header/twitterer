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
bindlogger = getLogger("bind")
bindlogger.setLevel(DEBUG)
bindlogger.addHandler(handler)


logger.debug("set up.")

print(setting.DISCORD_WEBHOOK)
