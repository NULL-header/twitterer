# encoding:utf-8


class Bind(object):
    def __init__(self):
        self.data = {}

    def read_data(self, path_data, path_err):
        result = 0
        try:
            with open(path_err, "r")as f:
                data = f.readlines()
        except Exception:
            result = 201
            return result
        try:
            with open(path_data, "r")as f:
                pass
            result = 100
        except Exception:
            result = 302
        buff = []
        for i in data:
            bu = i.rstrip().split(":")
            buff.append(tuple([int(bu[0]), bu[1]]))
        self.err = dict(buff)
        return result

    def set_bind(self, gid, cid):
        d = self.data
        if not d.get(gid):
            d[gid] = {}
        if d[gid].get(cid):
            return 301
        d[gid][cid] = self._childer()
        return 100

    @staticmethod
    def _childer():
        return{
            "tw": None,
            "id": None,
            "slug": None
        }

    def returner(self, code):
        return self.err[code]
