# encoding:utf-8
from logging import DEBUG, FileHandler, Formatter, StreamHandler, getLogger

import discord
import tweepy
from discord.ext import commands

logger = getLogger("main").getChild(__name__)


class Bot():
    def __init__(self):
        logger.debug("some setting on init")
        self.bot = commands.Bot(command_prefix=("!"),
                                description="simple my twitterer bot.")

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
