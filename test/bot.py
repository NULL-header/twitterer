# encoding:utf-8
import discord
from discord.ext import commands


def read_keys(path: str) -> dict:
    with open(path, "r")as f:
        text = f.readlines()
    list_dict = []
    for t in text:
        list_dict.append(tuple(t.split(":")))
    return dict(list_dict)


path_keys = "..\\.data\\key.txt"
keys = read_keys(path_keys)
