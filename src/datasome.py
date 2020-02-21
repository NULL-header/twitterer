class DataofCore(object):
    def __init__(self):
        self.__id = None
        self.__slug = None
        self.__twitter = None

    @property
    def twid(self):
        return self.__twid

    @twid.setter
    def twid(self, item):
        self.__twid = item

    @property
    def slug(self):
        return self.__slug

    @slug.setter
    def slug(self, item):
        self.__slug = item

    @property
    def twitter(self):
        return self.__twitter

    @twitter.setter
    def twitter(self, item):
        self.__twitter = item
