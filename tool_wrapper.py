import operator
import os
import pprint
import re
from collections import OrderedDict
from datetime import date, datetime
from os import getcwd as og
from os.path import join as oj

import simplejson as json
import tweepy
import twitter
from twython import Twython

# logging.debug(str(datetime.utcnow()))


# API key dictionary
tw_credentials = {
	"CONSUMER_KEY": 'Ok1mKcxNQWwX80KKIZZy1ouvU',
	"CONSUMER_SECRET": 'olcUdHvgK0AY40HPeyxiuunSNtG52qSqY4NIIZ23mpieMAoPIP',
	"ACCESS_KEY": '835204228859760641-nlxEx3Z3Hb9Gng2lpTVyDdxn1mJj3FN',
	"ACCESS_SECRET": 'nKjb64WWEJ1qfwP1iXY12kXzVuvePx2RPem74h80ZRTIc'
}

# API initialization
twapi = twitter.Api(
	consumer_key=tw_credentials['CONSUMER_KEY'],
	consumer_secret=tw_credentials['CONSUMER_SECRET'],
	access_token_key=tw_credentials['ACCESS_KEY'],
	access_token_secret=tw_credentials['ACCESS_SECRET'])

pass

# Twython API initialization
ty = Twython(
	app_key=tw_credentials['CONSUMER_KEY'],
	app_secret=tw_credentials['CONSUMER_SECRET'],
	oauth_token=tw_credentials['ACCESS_KEY'],
	oauth_token_secret=tw_credentials['ACCESS_SECRET'])

pp = pprint.PrettyPrinter(indent=4, compact=True)

tw_auth = tweepy.OAuthHandler(
	consumer_key=tw_credentials['CONSUMER_KEY'],
	consumer_secret=tw_credentials['CONSUMER_SECRET'],
)

tw_auth.set_access_token(
	key=tw_credentials['ACCESS_KEY'],
	secret=tw_credentials['ACCESS_SECRET']
)

twi = tweepy.API(tw_auth)


def dir_mkr(specified_path):
	if not os.path.isdir(specified_path):
		os.makedirs(specified_path)


def get_avatar_url(user, debug=True):
	try:
		
		# usr = twapi.GetUser(screen_name=name)
		
		usr = twi.get_user(user)
		
		if debug:
			# //db&t
			print(user)
		# //db&t
		
		for s in str(usr).split(', '):
			
			if "profile_image_url" in s:
				s = s.split(': ')[-1]
				
				avatar_url = s
				
				avatar_url = re.sub("'", '', avatar_url)
				
				return avatar_url
	
	# # //db&t
	# print(avatar_url)
	# # //db&t
	
	# avatar_url = re.match(r"", str(usr))
	
	# print(avatar_url)
	
	# break
	
	except:
		pass


def sort_objects(obj, sort_by_key='count'):
	# sorted(lis, key = lambda i: i['age'])
	
	obj = sorted(obj, key=lambda i: i[sort_by_key], reverse=True)
	
	return obj
	
	pass


def convert_old_mentions(fp):
	# with open(os.path.join(os.getcwd(), fp)) as JSR:
	#     mentions = dict(json.load(JSR))
	#
	# else:
	#     mentions = fp
	
	if isinstance(fp, dict):
		mentions = fp
	
	else:
		with open(os.path.join(os.getcwd(), fp)) as JSR:
			mentions = dict(json.load(JSR))
	
	lofmntz = []
	
	for k, v in mentions.items():
		info = {
			"twitter_handle": k.lower(),
			"avatar_url": '',
			"count": v
		}
		
		lofmntz.append(info)
	
	return lofmntz


# noinspection DuplicatedCode
def catch_up(old_file: os.path, new_file: os.path):
	with open(os.path.join(os.getcwd(), old_file)) as JSR:
		old_mentions = dict(json.load(JSR))
	
	with open(os.path.join(os.getcwd(), new_file)) as JSRo:
		new_mentions = list(json.load(JSRo))
	
	# list of dictionaries
	old_mentions = convert_old_mentions(old_mentions)
	
	accounted_for = [i['twitter_handle'].lower() for i in new_mentions]
	
	# for p in new_mentions:
	#     print(p)
	
	# print(accounted_for)
	
	COUNTER = 0
	
	KNT = 0
	
	for m in old_mentions:
		
		thand = m['twitter_handle'].lower()
		
		if thand not in accounted_for:
			
			COUNTER += 1
			
			m['avatar_url'] = get_avatar_url(thand)
			
			new_mentions.append(m)
			
			KNT += 1
			
			if COUNTER >= 100:
				break
	
	new_mentions = sort_objects(new_mentions)
	
	with open(os.path.join(os.getcwd(), 'mentions.json'), 'w') as JSW:
		JSW.write(json.dumps(new_mentions, indent=4))
	
	print("\n---------------\nadded %d values to file" % KNT)
	
	pass


def sort_old_mentions(file_path):
	with open(os.path.join(os.getcwd(), file_path)) as JSR:
		mentions = dict(json.load(JSR))
	
	mentions = dict(OrderedDict(sorted(mentions.items(), key=lambda x: x[0])))
	
	with open(os.path.join(os.getcwd(), 'mentions.json'), 'w') as JSW:
		JSW.write(json.dumps(mentions, indent=4))


def dedupe(file_path, otype: list = list):
	# noinspection PyGlobalUndefined
	global working_cp
	if otype is list:
		with open(os.path.join(os.getcwd(), file_path)) as JSR:
			mentions = list(json.load(JSR))
		
		working_cp = mentions
	
	elif otype is dict:
		
		with open(os.path.join(os.getcwd(), file_path)) as JSR:
			mentions = dict(json.load(JSR))
		
		working_cp = mentions
	
	else:
		quit()
	
	counter = {}
	
	# ordered dictionary method
	got = OrderedDict()
	
	if isinstance(working_cp, list):
		
		# noinspection PyUnboundLocalVariable
		for k in working_cp:
			
			o = k['twitter_handle'].lower()
			
			k['twitter_handle'] = k['twitter_handle'].lower()
			
			if o not in got:
				got[o] = k
			
			pass
		# //ordered dictionary method//
		
		for q in working_cp:
			
			th = q['twitter_handle'].lower()
			
			if th not in counter:
				
				counter[th] = 1
				
				pass
			
			elif th in counter:
				
				tcount = q['count']
				
				got[th]['count'] += tcount
				
				# print("%d -> %d" % (old_count, got[th]['count']))
				
				counter[th] += 1
		
		got = list(got.values())
		
		got = sort_objects(got)
	
	elif isinstance(working_cp, dict):
		
		# noinspection PyUnboundLocalVariable,PyUnboundLocalVariable
		for k, v in working_cp.items():
			
			k = k.lower()
			
			o = k
			
			if o not in got:
				got[o] = v
		
		for w, j in working_cp.items():
			
			w = w.lower()
			
			if w not in counter.keys():
				
				counter[w] = 1
			
			elif w in counter.keys():
				tcount = j
				
				got[w] += tcount
				
				# print("%d -> %d" % (old_count, got[th]['count']))
				
				counter[w] += 1
		
		# got = list(got.values())
		
		# # by mention count
		# got = OrderedDict(sorted(got.items(), key=operator.itemgetter(1), reverse=True))
		
		# alphabetically
		
		got = OrderedDict(sorted(got.items(), key=operator.itemgetter(0)))
	
	with open(os.path.join(os.getcwd(), 'mentions.json'), 'w') as JSW:
		JSW.write(json.dumps(got, indent=4))


# noinspection DuplicatedCode
def comparison(old_file: os.path = 'mentions.json', new_file: os.path = 'mentions.json'):
	with open(os.path.join(os.getcwd(), old_file)) as JSR:
		old_mentions = dict(json.load(JSR))
	
	with open(os.path.join(os.getcwd(), new_file)) as JSRo:
		new_mentions = list(json.load(JSRo))
	
	# list of dictionaries
	old_mentions = convert_old_mentions(old_mentions)
	
	old_handles = set()
	
	new_handles = set()
	
	for om in old_mentions:
		old_handles.add(om['twitter_handle'])
	
	for nm in new_mentions:
		new_handles.add(nm['twitter_handle'])
	
	print("---------------")
	
	print("%d remaining" % (len(old_handles) - len(new_handles)))
	
	pass


def convert_old(old_file: os.path, new_file: os.path):
	with open(os.path.join(os.getcwd(), old_file)) as JSR:
		old_mentions = JSR.read()[1:-1].split(', ')
		
		old_mentions = {s.split(": ")[0].split("'")[1]: {s.split(": ")[0].split("'")[1]: int(s.split(": ")[1])} for s in
		                old_mentions}
	
	with open(os.path.join(os.getcwd(), new_file)) as JSRo:
		new_mentions = list(json.load(JSRo))
	
	for nm in new_mentions:
		
		if nm['twitter_handle'] in old_mentions.keys():
			
			upd_count = list(old_mentions[nm['twitter_handle']].values())[0]
			
			if upd_count != nm['count']:
				print(upd_count, nm)


# noinspection PyUnusedLocal
def inc_ment(mentions_json_file=oj(og(), 'mentions.json'), parsed_tweets_file=oj(og(), 'parsed_ids.txt'), DBG=True,
             TST=False):
	append_parsed_tweets = open(parsed_tweets_file, 'a')
	
	with open(parsed_tweets_file, 'r') as rdr:
		read_parsed_tweets = [r.split('\n')[0] for r in rdr.readlines()]
	
	# if piff(mentions_json_file):
	
	if os.path.exists(mentions_json_file):
		with open(mentions_json_file, 'r') as JRD:
			tmp_dct = list(json.load(JRD))
	
	else:
		tmp_dct = None
	
	track_changes = []
	
	# convert mentions into an OrderedDict
	odct_mentions = OrderedDict()
	
	if tmp_dct:
		for c, m_obj in enumerate(tmp_dct):
			order_key = m_obj['twitter_handle']
			
			odct_mentions[order_key] = m_obj
	
	# # //db&t
	# if c >= 10:
	#     break
	# # //db&t
	
	for e, status in enumerate(twapi.GetHomeTimeline()):
		
		status_object = json.loads(str(status))
		
		unique_tweet_id = str(status_object['id'])
		
		# if the tweet id DOES exist in the parsed_tweets file, ignore it
		
		if unique_tweet_id in read_parsed_tweets and not TST:
			continue
		
		else:
			
			if not TST:
				append_parsed_tweets.write('%s\n' % unique_tweet_id)
			
			track_dct = {
				unique_tweet_id: []
			}
			
			for user_mentions in status_object['user_mentions']:
				
				screen_name = user_mentions['screen_name'].lower()
				
				track_dct[unique_tweet_id].append(screen_name)
				
				# if the twitter handle DOES exist inside of
				# the 'mentions_json', increment it's
				# count value by 1
				if screen_name in odct_mentions:
					
					odct_mentions[screen_name]['count'] += 1
				
				
				# if the twitter handle DOES NOT exist inside of
				# the 'mentions_json', create a new JSON object
				# for user BUT ensuring the structure of the
				# current of the OrderedDict we have temporarily implemented
				else:
					
					new_user_object = {
						"twitter_handle": screen_name,
						"avatar_url": "",
						"count": 1
					}
					
					odct_mentions[screen_name] = new_user_object
				
				# gets *LATEST* URL for user's avatar, is executed
				# everytime the username is encountered
				odct_mentions[screen_name]['avatar_url'] = get_avatar_url(screen_name, debug=False)
		
		track_changes.append(track_dct)
	
	append_parsed_tweets.close()
	
	# clean up OrderedDict: convert back to
	# standard dictionary structure, then
	# sort by count value
	reformatted_mentions = sort_objects(odct_mentions.values())
	
	# # //db&t
	# with open(os.path.join('/Users/chris/Desktop/ODCT.json'), 'w') as JSW:
	#     JSW.write(json.dumps(sort_objects(reformatted_mentions), indent=4))
	# # //db&t
	
	pass
	
	# # //db&t
	# pp.pprint(reformatted_mentions)
	# # //db&t
	
	print("%s: " % str(datetime.utcnow()).split('.')[0] + json.dumps(track_changes, indent=2))
	
	tchanges_dir = oj('tracked_changes')
	
	dir_mkr(tchanges_dir)
	
	date_changes_file = '%s_tracked_changes.log' % str(date.today())
	
	with open(oj(tchanges_dir, date_changes_file), 'a') as wrtr:
		wrtr.write("%s: " % str(datetime.utcnow()).split('.')[0] + json.dumps(track_changes, indent=2) + "\n")
	
	# for tc in track_changes:
	#
	#     logging.debug("Added tracked changes: %s" % str(tc))
	#
	#     # print("Added tracked changes: %s" % str(tc))
	#
	#
	#
	#     pass
	
	print(str(date.today()) + ": " + json.dumps(reformatted_mentions, indent=2))
	
	with open(mentions_json_file, 'w') as JWRT:
		JWRT.write(json.dumps(reformatted_mentions, indent=2))


def backlogged(list_of_file_paths):
	tracker = {}
	
	for fle in list_of_file_paths:
		
		with open(fle, 'r') as rdr:
			logged = rdr.readlines()
		
		for e, l in enumerate(logged):
			
			if re.search(r"^\s{6}\"(.*)\"", l):
				
				l = l.split("\"")[1]
				
				if l in tracker:
					
					tracker[l] += 1
				
				else:
					tracker[l] = 1
	
	# write changes from tracker to mentions.json
	with open('mentions.json', 'r') as JRD:
		tmp_dct = list(json.load(JRD))
	
	odct_mentions = OrderedDict()
	
	for c, m_obj in enumerate(tmp_dct):
		order_key = m_obj['twitter_handle']
		
		odct_mentions[order_key] = m_obj
	
	for k, v in tracker.items():
		
		if k in odct_mentions:
			
			odct_mentions[k]['count'] += v
		
		# print(odct_mentions[k])
		
		else:
			
			odct_mentions[k] = {
				'twitter_handle': k,
				# odct_mentions[screen_name]['avatar_url'] = get_avatar_url(screen_name, debug=False)
				'avatar_url': get_avatar_url(k, debug=False),
				'count': v
			}
	
	# print(odct_mentions[k])
	
	with open('mentions.json', 'w') as JWRT:
		JWRT.write(json.dumps(sort_objects(odct_mentions.values()), indent=2))
	
	pass


def test_pp(limit=20):
	mentions_json_file = "mentions.json"
	
	with open(mentions_json_file, 'r') as JRD:
		tmp_dct = list(json.load(JRD))
	
	for e, k in enumerate(tmp_dct):
		
		# pp.pprint(k)
		
		print("\t" + json.dumps(k, indent=4) + "\t")
		
		if e >= limit:
			break


log_files = [
	"/Users/chris/Desktop/twitter-mentions-scrape/cron-logs/15@cron-2018-06-17.log.txt",
	"/Users/chris/Desktop/twitter-mentions-scrape/cron-logs/15@cron-2018-06-18.log.txt",
	"/Users/chris/Desktop/twitter-mentions-scrape/cron-logs/15@cron-2018-06-19.log.txt",
	"/Users/chris/Desktop/twitter-mentions-scrape/cron-logs/15@cron-2018-06-20.log.txt",
	"/Users/chris/Desktop/twitter-mentions-scrape/cron-logs/15@cron-2018-06-21.log.txt",
]

# backlogged(log_files)


# # LOGGING VARIABLES
#
# LOG_DIR = oj(og(), 'PYLOGS')
#
# dir_mkr(LOG_DIR)
#
# log_file = oj(LOG_DIR, 'mentions_pylog_%s.log' % str(date.today()))
#
# Path(log_file).touch()
#
#
# logging.basicConfig(filename=log_file, level=logging.DEBUG)
#
# # //LOGGING VARIABLES//
