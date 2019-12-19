# encoding:utf-8

dict_tst = {}
dict_tst["tuika"] = []
dict_tst["tuika"].append("neko")
with open("..\.data\key.txt", "r")as f:
    text = f.readlines()
list_dict = []
for t in text:
    list_dict.append(tuple(t.split(":")))
dict_keys = dict(list_dict)
print(dict_keys)
