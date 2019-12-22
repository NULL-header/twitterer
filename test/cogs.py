# encoding:utf-8
from logging import getLogger

from discord.ext import commands

logger = getLogger("bot").getChild(__name__)


class Cmds(commands.Cog):
    def __init__(self, bot):
        logger.debug("class cmds starts up.")
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        logger.debug("check test.")
        await ctx.send("OK, master!")


def setup(bot):
    logger.debug("load class Cmds.")
    bot.add_cog(Cmds(bot))
