import subprocess
import sys
from logging import NullHandler, getLogger

from discord.ext import commands

logger = getLogger("bot")
logger.addHandler(NullHandler())


EXTENSIONS = [
    "cogs"
]


class Bot(commands.Bot):
    def __init__(self, dict_keys: dict, *, prfix: str = "!DEFAULT!"):
        logger.debug(f"class Bot setting prfix to {prfix} on init.")
        super().__init__(prfix)
        self.prfix = prfix
        self.dict_keys = dict_keys
        self.isFailedCogs = False
        for cog in EXTENSIONS:
            try:
                self.load_extension(cog)
                logger.debug("{0} could road.".format(cog))
            except Exception:
                stringerror = sys.exc_info()
                logger.warning("cog could not road;\n\n" +
                               f"with this trackback:{stringerror}\n")
                self.isFailedCogs = True

    async def on_ready(self):
        user_myself = self.user
        logger.debug(f"---Loged in as {user_myself.name}({user_myself.id})---")
        if self.prfix == "!DEFAULT!":
            logger.debug("restart up app.")
            cmd = f"python src/app.py !{self.user.name}!"
            subprocess.Popen(cmd.split())
            await self.logout()
        else:
            logger.debug(f"prefix is {self.prfix}")
        if self.isFailedCogs:
            await self.logout()

    async def on_message(self, msg):
        pass

    def wake(self):
        self.run(self.dict_keys["DISCORD_TOKEN"])
