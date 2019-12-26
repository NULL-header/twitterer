# encoding:utf-8

import os
import subprocess
import sys
import time

args = sys.argv
cmd1 = "which python"
cmd2 = "python test4.py check"
if len(args) == 1:
    print("I have no args.")
    subprocess.run(cmd1.split())
    subprocess.Popen(cmd2.split())
    print("check")
    while True:
        print("checker")
        time.sleep(1)
else:
    print("I have the {0}".format(args[1]))
    subprocess.run(cmd1.split())
