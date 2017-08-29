#!/usr/bin/python3
import json
import os
import shutil
import sys

def unicode_truncate(s, length=165):
    while (sys.getsizeof(s) > length):
        s = s[:-1]
    return s

try:
    shutil.rmtree("complex_names")
except:
    pass
os.mkdir("complex_names")

with open("blns.json", "r") as f:
    j = f.read()

names = json.loads(j)
os.chdir("complex_names")

dirs = set()
files = set()
failed = set()

i = 1

for name in names:
    _name = name
    if '/' in _name or _name == '.' or _name == '':
        continue
    try:
        os.mkdir(_name)
        dirs.add(_name)
    except Exception as err1:
        if "File name too long" in str(err1):
            try:
                os.mkdir(unicode_truncate(name))
                _name = unicode_truncate(name)
                dirs.add(_name)
            except Exception as err2:
                failed.add(_name)
                print(err2)
                continue
    try:
        with open("%s/%s" % (_name, _name), "w") as f:
            f.write(str(i))
        with open("%s/test.txt" % _name, "w") as f:
            f.write(str(i))
        files.add(_name)
        i += 1
    except Exception as err3:
        print(err3)
        pass

with open("test.txt", "w") as f:
    f.write("root")

print(failed)
print(dirs.difference(files))
print(files.difference(dirs))
