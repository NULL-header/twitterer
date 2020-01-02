# coding:utf-8


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
        self.__twitterer = arg

    @property
    def slug(self) -> str:
        return self.__twitterer

    @slug.setter
    def slug(self, arg: str):
        self.__twitterer = arg


a = DataBase(twitterer=Mytwitterer())
print(a)
