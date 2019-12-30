# encoding:utf-8
import asyncio
import os
import subprocess
import sys
from logging import NullHandler, getLogger

import discord
from discord.ext import commands

logger = getLogger("bot")
logger.addHandler(NullHandler())


EXTENSIONS = [
    "cogs"
]


class Bot(commands.Bot):
    def __init__(self, dict_keys: dict, *, prfix: str = "!DEFAULT!"):
        logger.debug("class Bot setting prfix to {0} on init.".format(prfix))
        super().__init__(prfix)
        self.prfix = prfix
        self.dict_keys = dict_keys
        for cog in EXTENSIONS:
            try:
                self.load_extension(cog)
                logger.debug("{0} could road.".format(cog))
            except Exception:
                logger.warning("cog could not road;\n\n"
                               "with this trackback:{0}\n"
                               .format(sys.exc_info()))

    async def on_ready(self):
        logger.debug("---Loged in as {0.name}({0.id})---".format(self.user))
        if(self.prfix == "!DEFAULT!"):
            logger.debug("restart up app.")
            cmd = "python app.py !{}!".format(self.user.name)
            subprocess.Popen(cmd.split(), shell=True)
            await self.logout()
        else:
            logger.debug("prefix is {}".format(self.prfix))

    def wake(self):
        self.run(self.dict_keys["token"])
