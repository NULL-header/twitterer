from logging import getLogger, NullHandler
import tweepy

logger = getLogger("twitter")
logger.addHandler(NullHandler())


class Mytwitter(object):
    counter = 0
    path_ram = ".data"

    def __init__(self, CK, CS, AT, AS):
        if not (Mytwitter.counter):
            self.__CK = CK
            self.__CS = CS
            self.__AT = AT
            self.__AS = AS
            self.get_oauth()
            Mytwitter.counter += 1

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__

    def get_oauth(self):
        auth = tweepy.OAuthHandler(self.__CK, self.__CS)
        auth.set_access_token(self.__AT, self.__AS)
        self.__api = tweepy.API(auth)

    @property
    def api(self):
        return self.__api

    def search_list(self, id: str) -> list:
        try:
            listlist = []
            for i in self.api.lists_all(id):
                listlist.append(i.name)
            return listlist
        except Exception:
            logger.warning("cannot read list from twitter id.")
            return None
