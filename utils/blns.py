#!/usr/bin/python3
import json
import os
import shutil
import sys

try:
    shutil.rmtree("data")
except:
    pass
os.mkdir("data")

with open("blns.json", "r") as f:
    j = f.read()

names = json.loads(j)
os.chdir("data")

dirs = set()
files = set()

i = 1

for name in names:
    if '/' in name:
        continue
    try:
        os.mkdir(name)
        dirs.add(name)
    except:
        pass
    try:
        with open("%s/%s" % (name, name), "w") as f:
            f.write(str(i))
            files.add(name)
        with open("%s/test.txt" % name, "w") as f:
            f.write(str(i))
        i += 1
    except:
        pass

with open("test.txt", "w") as f:
    f.write("root")

print(dirs.difference(files))
print(files.difference(dirs))
