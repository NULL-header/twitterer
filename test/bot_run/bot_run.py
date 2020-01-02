# coding:utf-8
from discord.ext import commands


class Mytwitterer():
    def __init__(self):
        pass


class DataBase():
    def __init__(self, *, twitterer=None, id=None, slug=None):
        self.__twitterer = twitterer
        self.__id = id
        self.__slug = slug

    @property
    def twitterer(self) -> Mytwitterer:
        return self.__twitterer

    @twitterer.setter
    def twitterer(self, arg: Mytwitterer):
        self.__twitterer = arg

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, arg: str):
        self.__id = arg

    @property
    def slug(self) -> str:
        return self.__slug

    @slug.setter
    def slug(self, arg: str):
        self.__slug = arg


if __name__ == "__main__":
    gid = "test_guild"
    channel = "test_channel"

    a = {}

    a[gid] = {}
    a[gid][channel] = DataBase()
    short1 = a[gid][channel]
    print(short1)
    print(short1.id)
    print(short1.slug)
    print(short1.twitterer)
    short1.id = "example"
    short1.slug = "testlist"
    short1.twitterer = Mytwitterer()
    print(short1)
    print(short1.id)
    print(short1.slug)
    print(short1.twitterer)
