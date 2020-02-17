from logging import getLogger
from discord.ext import commands
from func import Core
logger = getLogger("bot").getChild(__name__)
emoji = "\U0001F9E1"


class Cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.core = Core()

    @commands.command()
    async def test(self, ctx):
        logger.debug("check test")
        await ctx.send("OK, {0} !".format(ctx.message.author))

    @commands.command()
    async def sleep(self, ctx):
        await ctx.send("I'll sleep.")
        logger.debug("stoped.")
        await self.bot.logout()

    @commands.command()
    async def set_channel(self, ctx):
        self.core.setter(ctx.channel.id)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            logger.debug("my message.")
        elif msg.content.startswith(self.bot.prfix+"set_channel"):
            await self.bot.process_commands(msg)
            logger.debug("masaka")
        else:
            if self.core.checker(msg.channel.id):
                logger.debug("ok")
                await self.bot.process_commands(msg)


def setup(bot):
    logger.debug("load class Cmds.")
    bot.add_cog(Cmds(bot))
