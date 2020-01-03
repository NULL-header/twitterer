# encoding:utf-8
import os
import pickle
import subprocess
import sys
from logging import getLogger

from discord.ext import commands
from twitterer import Mytwitterer

logger = getLogger("bot").getChild(__name__)
path_bind = "..\\.data\\bind.pickle"
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
    "     It restert itself with new entered prefix as argment.\n"\
    "id:\n"\
    "     It put the entered twitter id in the list.\n"\
    "list:\n"\
    "     It can use when id which of the account have a target list is\n"\
    "    entered.\n"\
    "     It receive two argment, but it can work on single this.\n"\
    "     When it receive one, it search list which the received id have.\n"\
    "    Select in displayed lists; The list is put in the lists-list.\n"\
    "     When it receive two argments, this function recongnize first\n"\
    "    item as id, second item as list-name. And this list of the id is\n"\
    "    put in the lists-list."


class Cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.botcmds()
        if os.path.exists(path_bind):
            with open(path_bind, "rb")as f:
                self.bind_channel = pickle.load(f)
            logger.debug("could read bind.pickle.")
        else:
            self.bind_channel = {}
            logger.debug("could not read bind.pickle.")

    @staticmethod
    def childer(*, id: str = None, slug: str = None,
                twitterer: str = None) -> dict:
        return {
            "id": id,
            "slug": slug,
            "twitterer": twitterer,
        }

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
        bcg = self.bind_channel[str(ctx.guild.id)]
        items = bcg[self.indexer(ctx.channel.id, bcg)]
        if not items[1:]:
            items.append("")
        di = self.bot.dict_keys
        items[1] = Mytwitterer(di["CK"], di["CS"], di["AT"], di["AS"])
        await ctx.send("set ready.")
        logger.debug(self.bind_channel)

    @setter.command(name="id")
    async def set_id(self, ctx, id: str = None):
        if not id:
            await ctx.send("please put a id.")
            return
        if id.startswith("@"):
            id = id[1:]
        bcg = self.bind_channel[str(ctx.guild.id)]
        items = bcg[self.indexer(ctx.channel.id, bcg)]
        if not items[1:]:
            await ctx.send("please set ready command.")
            return
        if not items[2:]:
            items.append("")
        items[2] = id
        logger.debug(self.bind_channel)
        await ctx.send("set {} as twitter id.".format(id))
        self.dumper(path_bind, self.bind_channel)

    @setter.command(name="list")
    async def set_list(self, ctx, listname: str = None):
        bcg = self.bind_channel[str(ctx.guild.id)]
        items = bcg[self.indexer(ctx.channel.id, bcg)]
        listlist = items[1].search_list(items[2])
        if listname:
            pass
        else:
            namelist = []
            chan = ctx.channel
            for i in listlist:
                namelist.append(i.name)
            for i in namelist:
                await ctx.send(i)

            def check(m):
                return m.content in namelist and m.channel == chan

            msg = await self.bot.wait_for("message", check=check)
            items.append(msg.content)
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
        if not self.bind_channel[gid].get(ctx.channel.id):
            await ctx.send("here is binded.")
            self.bind_channel[gid][ctx.channel.id] = childer()
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
                         "with this trackback:{}\n".format(sys.exc_info))
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
                    if self.inchecker(
                            msg.channel.id, self.bind_channel.get(gid)):
                        if msg.content.startswith(self.bot.prfix):
                            logger.debug("the message has a command.")
                            await self.bot.process_commands(msg)
                        else:
                            logger.debug("no command.")
                            await msg.add_reaction(emoji)


def setup(bot):
    logger.debug("load class Cmds.")
    bot.add_cog(Cmds(bot))
