# encoding:utf-8


class Bind(object):
    path_data = "..\\.data\\aa"
    path_err = "..\\.data\\errcode.txt"

    def __init__(self):
        self.data = {}

    def read_data(self):
        try:
            with open(Bind.path_err, "r")as f:
                data = f.readlines()
        except Exception:
            return 1
        buff = []
        for i in data:
            buff.append(tuple(i.rstrip().split(":")))
        self.err = dict(buff)
        print(self.err)
        return 0

    def set_bind(self, gid, cid):
        d = self.data
        if not d.get(gid):
            d[gid] = {}
        if d[gid].get(cid):
            return 1
        d[gid][cid] = self._childer()
        return 0

    @staticmethod
    def _childer():
        return{
            "tw": None,
            "id": None,
            "slug": None
        }

    def _returner(self, code):
        pass
