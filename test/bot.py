# encoding:utf-8
import sys
from logging import NullHandler, getLogger

import discord
import tweepy
from discord.ext import commands

logger = getLogger("bot")
logger.addHandler(NullHandler())

EXTENSIONS = [
    "cogs"
]


class Bot(commands.Bot):
    def __init__(self, *, prfix="!DEFAULT!"):
        logger.debug("class Bot setting prfix to {0} on init.".format(prfix))
        super().__init__(prfix)
        logger.debug("load cogs.")
        for cog in EXTENSIONS:
            try:
                self.load_extension(cog)
                logger.debug("{0} could road.".format(cog))
            except Exception:
                logger.error("could not road;\n\n"
                             "with this trackback:{0}".format(sys.exc_info()))

    async def on_ready(self):
        logger.debug("---Loged in as {0.name}({0.id})---".format(self.user))
