# encoding:utf-8
import tweepy


class Mytwitterer():
    counter = 0

    def __init__(self, CK, CS, AT, AS):
        if not (Mytwitterer.counter):
            self.__CK = CK
            self.__CS = CS
            self.__AT = AT
            self.__AS = AS
            self.get_oauth()
            Mytwitterer.counter += 1

    def get_oauth(self):
        auth = tweepy.OAuthHandler(self.__CK, self.__CS)
        auth.set_access_token(self.__AT, self.__AS)
        self.__api = tweepy.API(auth)

    @property
    def api(self):
        return self.__api
