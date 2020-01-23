# encoding:utf-8
import os
import pickle
import subprocess
import sys
from logging import getLogger

from bind import Bind
from discord.ext import commands
from twitterer import Mytwitterer

logger = getLogger("bot").getChild(__name__)
path_bind = ".data\\bind.pickle"
path_err = ".data\\errcode.txt"
emoji = "\U0001F9E1"

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
        self.botcmds()
        self.bind = Bind()
        data_dict = {
            "pd": path_bind,
            "ck": self.bot.dict_keys["CK"],
            "cs": self.bot.dict_keys["CS"],
            "at": self.bot.dict_keys["AT"],
            "as": self.bot.dict_keys["AS"],
        }
        self.bind.setter(data_dict)
        self.bind.read_data()

    def dumper(self, path: str, arg: dict):
        with open(path, "wb")as f:
            pickle.dump(self.bind_channel, f)

    @commands.command()
    async def test(self, ctx):
        logger.debug("check test.")
        await ctx.send("OK, {0} !".format(ctx.message.content))

    @commands.group(name="set")
    async def setter(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(set_disp)

    @setter.command(name="prefix")
    async def set_prefix(self, ctx, prfix: str = None):
        if not prfix:
            await ctx.send("Please put a prefix.")
        else:
            await ctx.send("restart.")
            cmd = "python app.py {}".format(prfix)
            subprocess.Popen(cmd.split(), shell=True)
            await self.bot.logout()

    @setter.command(name="ready")
    async def set_ready(self, ctx):
        items = self.bind_channel[str(ctx.guild.id)][str(ctx.channel.id)]
        di = self.bot.dict_keys
        items["twitterer"] = \
            Mytwitterer(di["CK"], di["CS"], di["AT"], di["AS"])
        await ctx.send("set ready.")
        logger.debug(self.bind_channel)

    @setter.command(name="id")
    async def set_id(self, ctx, id: str = None):
        if not id:
            await ctx.send("please put a id.")
            return
        if id.startswith("@"):
            id = id[1:]
        items = self.bind_channel[str(ctx.guild.id)][str(ctx.channel.id)]
        if not items["twitterer"]:
            await ctx.send("please set ready command.")
            return
        items["id"] = id
        logger.debug(self.bind_channel)
        await ctx.send("set {} as twitter id.".format(id))
        self.dumper(path_bind, self.bind_channel)

    @setter.command(name="list")
    async def set_list(self, ctx, listname: str = None):
        items = self.bind_channel[str(ctx.guild.id)][str(ctx.channel.id)]
        listlist = items["twitterer"].search_list(items["id"])
        if listname:
            if listname in listlist:
                items["slug"] = listname
        else:
            chan = ctx.channel
            for i in listlist:
                await ctx.send(i)

            def check(m):
                return m.content in listlist and m.channel == chan
            msg = None
            while not msg:
                try:
                    msg = await self.bot.wait_for("message", check=check)
                except Exception:
                    await ctx.send("That message is invalid.")
            items["slug"] = msg.content
        await ctx.send("Set list.")
        logger.debug(self.bind_channel)

    @commands.command()
    async def sleep(self, ctx):
        logger.debug("stoped.")
        await self.bot.logout()

    @commands.group()
    async def bind(self, ctx):
        logger.debug("bind set wakes up.")
        if ctx.invoked_subcommand is None:
            await ctx.send(bind_disp)

    @bind.command(name="set")
    async def set_bind(self, ctx):
        gid = str(ctx.guild.id)
        if not self.bind_channel.get(gid):
            self.bind_channel[gid] = {}
        if not self.bind_channel[gid].get(str(ctx.channel.id)):
            await ctx.send("here is binded.")
            self.bind_channel[gid][str(ctx.channel.id)] = self.childer()
            self.dumper(path_bind, self.bind_channel)
        else:
            await ctx.send("here was binded, yet.")
        logger.debug(self.bind_channel)

    @bind.command(name="clean")
    async def clean_bind(self, ctx):
        self.bind_channel = {}
        try:
            os.remove(path_bind)
            await ctx.send("clean up.")
            logger.debug(self.bind_channel)
        except Exception:
            logger.debug("no item on path_bind;\n\n"
                         "with this trackback:{}\n".format(sys.exc_info()))
            await ctx.send("cleaned up, yet.")

    def botcmds(self):
        @self.bot.check
        async def block_dm(ctx):
            return ctx.guild is not None

        @self.bot.event
        async def on_message(msg):
            if msg.author == self.bot.user:
                logger.debug("my message.")
            elif msg.content.startswith(self.bot.prfix + "bind"):
                await self.bot.process_commands(msg)
            else:
                gid = str(msg.guild.id)
                if self.bind_channel.get(gid):
                    if self.bind_channel[gid].get(str(msg.channel.id)):
                        if msg.content.startswith(self.bot.prfix):
                            logger.debug("the message has a command.")
                            await self.bot.process_commands(msg)
                        else:
                            logger.debug("no command.")
                            await msg.add_reaction(emoji)


def setup(bot):
    logger.debug("load class Cmds.")
    bot.add_cog(Cmds(bot))
