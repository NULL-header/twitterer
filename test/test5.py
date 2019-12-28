# encoding:utf-8
import os
import pickle

if(1 != 1):
    print("check1")
if(1 == 1):
    print("check2")
else:
    print("check3")


def Gen():
    i = 0
    while True:
        yield str(i)
        i += 1


gen1 = Gen()
gen2 = Gen()
path = "..\\.data\\test1.pickle"


def Gen2():
    gen = Gen()
    check1 = path + gen.__next__()
    while os.path.exists(check1):
        check1 = path + gen.__next__()
    i = int(gen.__next__()) - 1
    while True:
        yield str(i)
        i += 1


gen3 = Gen2()
list_ = [0, 1, 2, 3, 4]

for i in list_:
    with open(path + gen1.__next__(), "wb")as f:
        pickle.dump(i, f)

with open(path + "0", "rb")as f:
    a = pickle.load(f)

print(a)
print(type(a))

list_new = []
check = path + gen2.__next__()
while os.path.exists(check):
    with open(check, "rb")as f:
        list_new.append(pickle.load(f))
    check = path + gen2.__next__()

print(list_new)

for i in list_new:
    with open(path + gen3.__next__(), "wb")as f:
        pickle.dump(i, f)
