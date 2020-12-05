import re
import os
import json
from pathlib import Path, PureWindowsPath

with open(
        "C:/Users/thick/Dropbox/[Programming]/Portfolio_[working-on]/mentions-counter-2018-05-03/mentions.json") as js_reader:
    jsobj = json.load(js_reader)

for e, i in enumerate(jsobj):
    # print()
    print("%d: %s" % (e, str(i)))
    # print(e + ": " + i)
    # print()
    
    if e == 10:
        break
