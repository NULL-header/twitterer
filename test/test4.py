# encoding:utf-8

import subprocess
import sys

args = sys.argv
cmd1 = "which python"
cmd2 = "python test4.py check"
if len(args) == 1:
    a = input()
    print("I have no args.")
    subprocess.run(cmd1.split())
    subprocess.run(cmd2.split())
else:
    print("I have the {0}".format(args[1]))
