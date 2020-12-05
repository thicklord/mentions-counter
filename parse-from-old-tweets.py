import json
import re
from os.path import join as oj

import pandas as pd

tweets_file = oj('tweets-original.csv')

df = pd.read_csv(tweets_file, usecols=['text'])


LIMIT = 15

capture = re.compile(r"@[\w]+")

mentions_d = {}

# goes over old tweets and counts mentions
for i, r in df.iterrows():
    
    text = str(r['text'])
    
    caught = capture.findall(text)
    
    for c in caught[1:]:
        #
        # print(c)
        #
        # continue
        
        c = str(c[1:]).lower()
        
        if c in mentions_d:
            mentions_d[c] += 1
        
        else:
            mentions_d[c] = 1

    # if i >= LIMIT:
    #     break

# open mentions.json

with open('mentions@bak.json', 'r') as mj:
    mdict = dict(json.load(mj))

for k, v in mentions_d.items():

    if k in mdict:
        mdict[k] += v
        
        print(k)
        
        # print(mdict[k])
    else:
        mdict[k] = v


with open('mentions.json', 'w') as jw:
    jw.write(json.dumps(mdict))








