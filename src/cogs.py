from logging import getLogger
from discord.ext import commands
from func import Core
import subprocess
import asyncio
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
        self.is_stocker_run = False
        self.core = Core()
        items = {
            "path": path_save,
            "Ck": self.bot.dict_keys["CONSUMER_KEY"],
            "Cs": self.bot.dict_keys["CONSUMER_SERCRET"],
            "At": self.bot.dict_keys["ACCESS_TOKEN"],
            "As": self.bot.dict_keys["ACCESS_TOKEN_SERCRET"],
        }
        self.core.setter(**items)
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
            await ctx.send("seted id.")
            return
        await ctx.send("Please put a prefix.")

    @setter.command(name="list")
    async def set_slug(self, ctx, slug=None):
        if not self.core.binded_channel[ctx.channel.id].twid:
            await ctx.send("Please set a id before setting the list.")
            return
        listlist = self.core.catch_lists(ctx.channel.id)
        if not listlist:
            await ctx.send("Please set a id before setting the list.")
            return
        if slug:
            if not listlist:
                await ctx.send("Lists can not be search.")
                return
            if slug in listlist:
                self.core.set_list(slug)
            else:
                item = self.core.binded_channel[ctx.channel.id]
                await ctx.send(("The {0} does not exist on the account which" +
                                " has the id {1}").format(slug, item.twid))
        else:
            for i in listlist:
                await ctx.send(i)
            channel = ctx.channel

            def check(m):
                return m.content in listlist and m.channel == channel

            msg = None
            while not msg:
                msg = await self.bot.wait_for("message", check=check)
                if not msg:
                    await ctx.send("That message is invalid.")
            self.core.set_list(channel.id, msg.content)
        await ctx.send("Set list.")

    @commands.group(name="switch")
    async def switch_for_loop_method(self, ctx):
        pass

    @switch_for_loop_method.command(name="start")
    async def stocker_starter(self, ctx):
        pass

    @switch_for_loop_method.command(name="start")
    async def stocker_stoper(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            logger.debug("my message.")
        elif msg.content.startswith(self.bot.prfix+"bind"):
            await self.bot.process_commands(msg)
        else:
            if self.core.checker(msg.channel.id):
                await self.bot.process_commands(msg)

    async def stocker(self):
        if self.is_stocker_run:
            logger.debug("stocker wake up.")
            await asyncio.sleep(60)
            asyncio.ensure_future(self.stocker())
        logger.debug("stocker stopped.")


def setup(bot):
    logger.debug("load class Cmds.")
    bot.add_cog(Cmds(bot))
