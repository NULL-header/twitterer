# encoding:utf-8
import json
import os
import subprocess
import sys
from logging import getLogger

from discord.ext import commands

from .twitterer import Mytwitterer

logger = getLogger("bot").getChild(__name__)
path_bind = "..\\.data\\bind.json"
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
    "    put in the lists-list."\



class Cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.botcmds()
        if os.path.exists(path_bind):
            with open(path_bind, "r")as f:
                self.bind_channel = json.load(f)
            logger.debug("could read bind.json.")
        else:
            self.bind_channel = {}
            logger.debug("could not read bind.json.")

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

    @setter.command(name="id")
    async def set_id(self, ctx, id: str = None):
        if not id:
            await ctx.send("Put a id.")
            return

    @setter.command(name="list")
    async def set_list(self, ctx, id: str = None, *, listname: str = None):
        if not id:
            await ctx.send("Put a list.")
            return
        if listname:
            pass
        else:
            pass

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
            self.bind_channel[gid] = []
        if ctx.channel.id not in self.bind_channel[gid]:
            await ctx.send("here is binded.")
            self.bind_channel[gid].append(ctx.channel.id)
            with open(path_bind, "w")as f:
                json.dump(self.bind_channel, f, indent=4)
        else:
            await ctx.send("here was binded, yet.")
        logger.debug(self.bind_channel)

    @bind.command(name="clean")
    async def clean_bind(self, ctx):
        self.bind_channel = {}
        try:
            os.remove(path_bind)
        except Exception:
            logger.debug("no item on path_bind;\n\n"
                         "with this trackback:{}\n".format(sys.exc_info))

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
                    if msg.channel.id in self.bind_channel.get(gid):
                        if msg.content.startswith(self.bot.prfix):
                            logger.debug("the message has a command.")
                            await self.bot.process_commands(msg)
                        else:
                            logger.debug("no command.")
                            await msg.add_reaction(emoji)


def setup(bot):
    logger.debug("load class Cmds.")
    bot.add_cog(Cmds(bot))
