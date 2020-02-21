from logging import getLogger
from discord.ext import commands
from func import Core
import subprocess
logger = getLogger("bot").getChild(__name__)
emoji = "\U0001F9E1"
path_save = ".data/savedata.txt"
bind_disp = \
    "-----command list-----\n"\
    "set:\n"\
    "     It put the channel where the command sended to the list.\n"\
    "     Other commands can only work on the channel in it.\n"\
    "clean:\n"\
    "     It delete channel-ids from the list.\n"

set_disp =\
    "-----command list-----\n"\
    "prefix:\n"\
    "     It restart itself with new entered prefix as argment.\n"\
    "ready:\n"\
    "     It set internal data with twitter Oauth authentication on first.\n"\
    "id:\n"\
    "     It put the entered twitter id in the internal data.\n"\
    "list:\n"\
    "     It can use when id which of the account have the target list is\n"\
    "    entered.\n"\
    "     It recieve one argument, but it can work without this item.\n"\
    "     When it do not receive any of arguments, this function search\n"\
    "    some lists which the account of the id have.\n"\
    "    Select in displayed lists; the list is put to internal data.\n"\
    "     When it get a argment, if there is string the argment in list\n"\
    "    which the account of the id in the data have, this function put\n"\
    "    this to internal data.\n"


class Cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.core = Core()
        self.core.setter(path=path_save)
        self.core.load_savedata()

    @commands.command()
    async def test(self, ctx):
        logger.debug("check test")
        await ctx.send("OK, {0} !".format(ctx.message.author))

    @commands.command()
    async def sleep(self, ctx):
        await ctx.send("I'll sleep.")
        logger.debug("stoped.")
        await self.bot.logout()

    @commands.group()
    async def bind(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(bind_disp)

    @bind.command(name="set")
    async def set_channel(self, ctx):
        if not self.core.bind(ctx.channel.id):
            await ctx.send("It is binded here, yet.")
            return
        await ctx.send("It is binded here now.")

    @bind.command(name="clean")
    async def clean_channel(self, ctx):
        self.core.clean()
        await ctx.send("Internal data is clean.")

    @commands.group(name="set")
    async def setter(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(set_disp)

    @setter.command(name="prfix")
    async def set_prfix(self, ctx, prfix: str = None):
        if prfix:
            await ctx.send("restert.")
            cmd = "python src/app.py {}".format(prfix)
            subprocess.Popen(cmd.split())
            await self.bot.logout()
        else:
            await ctx.send("Please put a prefix.")

    @setter.command(name="id")
    async def set_id(self, ctx, id_: str = None):
        if id_:
            self.core.set_id(ctx.channel.id, id_)
        else:
            await ctx.send("Please put a prefix.")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            logger.debug("my message.")
        elif msg.content.startswith(self.bot.prfix+"bind"):
            await self.bot.process_commands(msg)
        else:
            if self.core.checker(msg.channel.id):
                await self.bot.process_commands(msg)


def setup(bot):
    logger.debug("load class Cmds.")
    bot.add_cog(Cmds(bot))
