import argparse

parser = argparse.ArgumentParser(description='Process tweets.')

parser.add_argument('item_name', metavar='item_name',
                    type=str, nargs=1,
                    help='the item name')

parser.add_argument('tweet_file_path', metavar='tweet_file_path',
                    type=str, nargs=1,
                    help='the file path of the tweets')

parser.add_argument('item_file_path', metavar='item_file_path',
                    type=str, nargs=1,
                    help='the file path of the items')

parser.add_argument('--debug', '-d',dest='debug',
                    action='store_true', default=False,
                    help='show debug logs (default: hide debug logs)')

parser.add_argument('--num_entries', '-n', dest='num_entries',
                    type=int, default=-1,
                    help='number of entries to process (default: all)')

parser.add_argument('--output', '-o', dest='output_data',
                    action='store_true', default=False,
                    help='output the results (default: no output)')

args = parser.parse_args()

import json
import re
import urllib

class Twitter:
    def __init__(self, user, tweet, retweet_count, reply_count, like_count, timestamp):
        self.user = user
        self.tweet = tweet
        self.retweet_count = retweet_count
        self.reply_count = reply_count
        self.like_count = like_count
        self.timestamp = timestamp

with open(args.tweet_file_path[0]) as tweet_json:
    tweet_data = json.load(tweet_json)

entries = [Twitter(tweet['user'], tweet['text'], tweet['retweets'], tweet['replies'], tweet['likes'], tweet['timestamp']) for tweet in tweet_data]

if args.num_entries > -1:
    entries = entries[:args.num_entries]

item_file_name = args.item_file_path[0]
item_file = open(item_file_name, 'r')
itemid = ''

for line in item_file:
    if re.search(r'name:(.*?),', line).group(1) == args.item_name[0]:
        itemid = re.search(r'id:(.*?),', line).group(1)
        break

class Processed:
    def __init__(self, userid, productid, content, content_type, timestamp, source):
        self.userid = userid
        self.productid = productid
        self.content = content
        self.content_type = content_type
        self.timestamp = timestamp
        self.source = source

# Bios
bios = []
for entry in entries:
    try:
        url = "https://twitter.com/" + entry.user
        f = urllib.urlopen(url)
        page = f.read()
        bios.append(Processed(entry.user, itemid, re.search('<p class=\"ProfileHeaderCard-bio u-dir\" dir=\"ltr\">(.*)</p>', page).group(1), 'bio', entry.timestamp, 'twitter'))
    except:
        bios.append(Processed(entry.user, itemid, '', 'bio', entry.timestamp, 'twitter'))

# Tweets
tweets = []
retweet_counts = []
reply_counts = []
like_counts = []
for entry in entries:
    tweets.append(Processed(entry.user, itemid, entry.tweet, 'tweet', entry.timestamp, 'twitter'))
    retweet_counts.append(Processed(entry.user, itemid, entry.retweet_count, 'retweet count', entry.timestamp, 'twitter'))
    reply_counts.append(Processed(entry.user, itemid, entry.reply_count, 'reply count', entry.timestamp, 'twitter'))
    like_counts.append(Processed(entry.user, itemid, entry.like_count, 'like count', entry.timestamp, 'twitter'))

if args.debug:
    print 'Bios'
    for bio in bios:
        print bio
    print '\n'

    print 'Tweets'
    for tweet in tweets:
        print tweet
    print '\n'

    print 'Retweet count'
    for retweet_count in retweet_counts:
        print retweet_count
    print '\n'

    print 'Reply count'
    for reply_count in reply_counts:
        print reply_count
    print '\n'

    print 'Like count'
    for like_count in like_counts:
        print like_count
    print '\n'

import string
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

arrs = [bios, tweets, retweet_counts, reply_counts, like_counts]
if not args.output_data:
    if args.debug:
        print 'Not outputting to file'
else:
    if args.debug:
        print 'Outputting to file'
    for arr in arrs:
        for el in arr:
            print '"' + el.userid + '","' + el.productid + '","' + ''.join(l for l in el.content if l not in string.punctuation) + '","' + el.content_type + '","' + el.timestamp + '","' + el.source + '"'
