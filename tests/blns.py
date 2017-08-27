import json
import os

with open("blns.json", "r") as file:
    j = file.read()

names = json.loads(j)
os.chdir("data")
for name in names:
    try:
        os.mkdir(name)
    except:
        print("Can't create %s" % name)

    try:
        with open("%s/test.txt" % name) as file:
            file.write(name)
    except:
        print("Can't open %s" % name)
