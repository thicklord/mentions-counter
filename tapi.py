import json
from os.path import isfile as piff

import pandas as pd

from tool_wrapper import *

# API key dictionary
tw_credentials = {
    "CONSUMER_KEY": '',
    "CONSUMER_SECRET": '',
    "ACCESS_KEY": '',
    "ACCESS_SECRET": ''
}

# API initialization
twapi = twitter.Api(
    consumer_key=tw_credentials['CONSUMER_KEY'],
    consumer_secret=tw_credentials['CONSUMER_SECRET'],
    access_token_key=tw_credentials['ACCESS_KEY'],
    access_token_secret=tw_credentials['ACCESS_SECRET']
)


def parse_all_data():
    
    dlst = []
    
    for e, status in enumerate(twapi.GetHomeTimeline()):
        
        j_status = json.loads(str(status))
        
        try:
            
            print("Iteration: %d" % e)
            
            dta = {
                'tweet_id': str(j_status['id']),
                'in_reply_to_status_id': '',
                'in_reply_to_user_id': '',
                'timestamp': j_status['created_at'],
                'source': j_status['source'],
                'text': j_status['text'],
                'rt_id': str(j_status['retweeted_status']['id']),
                'rt_uid': str(j_status['retweeted_status']['user']['id']),
                'rt_ts': str(j_status['retweeted_status']['created_at']),
                'expanded_urls': [],
            }
        
            # if int(j_status['retweet_count']) > 0:
            #     dta['rt_id'] = j_status['retweeted_status']['id'],
            #     dta['rt_uid'] = j_status['retweeted_status']['user']['id'],
            #     dta['rt_ts'] = j_status['retweeted_status']['created_at'],
            
            if len(j_status['urls']) > 0:
            
                for i in j_status['urls']:
                    dta['expanded_urls'].append(i['expanded_url'])
            
        except (KeyError, TypeError):
        
            # # pretty prints json format
            # print(json.dumps(j_status, indent=4))
    
            dta = {
                'tweet_id': j_status['id'],
                'in_reply_to_status_id': '',
                'in_reply_to_user_id': '',
                'timestamp': j_status['created_at'],
                'source': j_status['source'],
                'text': j_status['text'],
                'rt_id': 'nan',
                'rt_uid': 'nan',
                'rt_ts': 'nan',
                'expanded_urls': [],
            }
        
        if not dta['expanded_urls']:
            dta['expanded_urls'] = 'nan'
        
        dlst.append(list(dta.values()))
        
        # # pretty prints json format
        # print(json.dumps(j_status, indent=4))
    return dlst


def mention_incrementer():
    # mentions JSON file path
    mentions_json = oj(og(), 'mentions.json')
    
    # parsed tweet IDs file path
    parsed_tweets = oj(og(), 'parsed_ids.txt')
    
    # opens parsed IDs file in append mode so we don't overwrite
    ids = open(parsed_tweets, 'a')
    
    # check existence of JSON file, if it exists
    # load it to a dictionary. if it doesn't,
    # use a blank dictionary
    if piff(mentions_json):
        with open(mentions_json, 'r') as mj:
            mdict = dict(json.load(mj))
    
    else:
        mdict = {}
    
    # read parsed tweet IDs in as a list for easy checking
    with open(parsed_tweets, 'r') as rd:
    
        prsd = rd.read()
    
    mdict = convert_old_mentions(mdict)
    
    for e, status in enumerate(twapi.GetHomeTimeline()):
        j_status = json.loads(str(status))
        
        tw_id = str(j_status['id'])
        
        if tw_id in prsd:
            
            # # //db&t
            # print("id exists")
            # # //db&t
    
            continue
        else:
            ids.write('%s\n' % tw_id)
        
        for um in j_status['user_mentions']:
            
            # print(um['screen_name'])
            
            sn = um['screen_name']

            # noinspection PyUnusedLocal
            existing_handles = [mdict['twitter_handle'] for m in mdict]
            
            if sn in existing_handles:
                
                
                
                # old
                mdict[sn] += 1
            
            else:
                mdict[sn] = 1
    
    ids.close()
    
    print(mdict)
    
    with open(mentions_json, 'w') as jw:
        jw.write(json.dumps(mdict))


def prepender():
    
    new_data = parse_all_data()
    
    df = pd.read_csv('tweets.csv', dtype=str)
    
    # df = df.apply(str)
    
    columns = list(df.columns.values)
    
    new_data = pd.DataFrame(new_data, columns=columns, dtype=str)
    
    new_data = new_data.applymap(str)
    
    # new_data = new_data.apply(str)
    
    merged = pd.concat([new_data, df])
    
    merged = merged.set_index('tweet_id')
    
    for c in list(merged.columns.values):
        
        merged[c] = merged[c].apply(str)
    
    merged.to_csv('tweets.csv')
    
    
prepender()

# mention_incrementer()

inc_ment()
