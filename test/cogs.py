# encoding:utf-8
import json
import os
import sys
from logging import getLogger

from discord.ext import commands

logger = getLogger("bot").getChild(__name__)
path_bind = "..\\.data\\bind.json"
emoji = "\U0001F9E1"

bind_disp = \
    "-----command list-----\n"\
    "set:\n"\
    "    it put the channel where the command sended to the list.\n"\
    "    other commands can work on the channel in the list.\n"\
    "clean:\n"\
    "    it delete channel id from list.\n"


class Cmds(commands.Cog):
    def __init__(self, bot):
        logger.debug("class cmds starts up.")
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

    @commands.command()
    async def prfix(self, ctx):
        prfix = await self.bot.get_prefix(ctx.message)
        logger.debug("check prefix {}".format(prfix))
        logger.debug("{}".format(type(prfix)))

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
        logger.debug("set function starts up.")
        if not self.bind_channel.get(gid):
            logger.debug("bind_channel[{}] clean up.".format(gid))
            self.bind_channel[gid] = []
        else:
            logger.debug("bind_channel[{}] exists.".format(gid))
        if ctx.channel.id not in self.bind_channel[gid]:
            logger.debug("bind channel.")
            await ctx.send("here is binded.")
            self.bind_channel[gid].append(ctx.channel.id)
            with open(path_bind, "w")as f:
                json.dump(self.bind_channel, f, indent=4)
        else:
            logger.debug("bind here, yet.")
            await ctx.send("here was binded, yet.")
        logger.debug(self.bind_channel)
        logger.debug("set finish.")

    @bind.command(name="clean")
    async def clean_bind(self, ctx):
        logger.debug("clean function starts up.")
        self.bind_channel = {}
        try:
            os.remove(path_bind)
        except Exception:
            logger.debug("no item on path_bind.")
        finally:
            logger.debug("clean function finished.")

    async def botcmds(self):
        def likes(msg):
            await mssage.add_reaction(emoji)

        @self.bot.check
        async def block_dm(ctx):
            logger.debug("check decorater worked.")
            return ctx.guild is not None

        @self.bot.event
        async def on_message(msg):
            logger.debug("saw a message.")
            if msg.author == self.bot.user:
                logger.debug("my message.")
            elif msg.content.startswith(self.bot.prfix + "bind"):
                logger.debug("bind set start up.")
                await self.bot.process_commands(msg)
            else:
                gid = str(msg.guild.id)
                logger.debug("check a bind.")
                if self.bind_channel.get(gid):
                    logger.debug("bind_channel[{}] exists".format(gid))
                    if msg.channel.id in self.bind_channel.get(gid):
                        if msg.content.startswith(self.bot.prfix):
                            logger.debug("the message has a command.")
                            await self.bot.process_commands(msg)
                        else:
                            logger.debug("no command.")
                            await likes(msg)
                    else:
                        logger.debug("the bot have no permissions.")
                else:
                    logger.debug("the bot have no binds.")


def setup(bot):
    logger.debug("load class Cmds.")
    bot.add_cog(Cmds(bot))
