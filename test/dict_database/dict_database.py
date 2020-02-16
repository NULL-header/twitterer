# coding:utf-8
import pickle

from discord.ext import commands


class Mytwitterer():
    def __init__(self):
        pass


def childer(arg: dict, *, id=None, slug=None, twitterer=None):
    arg["id"] = id
    arg["slug"] = slug
    arg["twitterer"] = twitterer


if __name__ == "__main__":
    gid = ["guildid1", "guildid2", "guildid3"]
    channel = ["guildid1_channel1",
               "guildid1_channel2",
               "guildid2_channel1", ]
    a = {}
    a[gid[0]] = {}
    a[gid[0]][channel[0]] = {}
    childer(a[gid[0]][channel[0]], id="test1", slug="test2")
    a[gid[0]][channel[1]] = {}
    childer(a[gid[0]][channel[1]], id="test3", twitterer=Mytwitterer())
    a[gid[1]] = {}
    a[gid[1]][channel[2]] = {}
    childer(a[gid[1]][channel[2]], id="test5", slug="test6")
    a[gid[2]] = {}

    print(a)

    with open("data.pickle", "wb")as f:
        pickle.dump(a, f)

    b = ""

    with open("data.pickle", "rb")as f:
        b = pickle.load(f)

    print(b)
