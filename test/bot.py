# encoding:utf-8
from logging import getLogger

import discord
import tweepy
from discord.ext import commands

logger = getLogger(__name__)


class Cmds(commands.Cog):
    def __init__(self, bot):
        logger.debug("class cmds starts up.")
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        logger.debug("check test")
        await ctx.send("OK, master!")


class Bot():
    def __init__(self, *, prfix="!"):
        logger.debug(" setting prefix to \"{0}\" on init.".format(prfix))
        self.bot = commands.Bot(command_prefix=(prfix),
                                description="simple my twitterer bot.")
        self.bot.add_cog(Cmds(self.bot))

    @staticmethod
    def read_keys(path: str) -> dict:
        with open(path, "r")as f:
            text = f.readlines()
        list_dict = []
        for t in text:
            list_dict.append(tuple(t.split(":")))
        return dict(list_dict)

    def run(self):
        @self.bot.event
        async def on_ready():
            logger.debug("Logged in as {0}({0.id})".format(self.bot.user))
            logger.debug("--------------------")
        self.bot.run(self.read_keys("..\\.data\\key.txt")["token"])
