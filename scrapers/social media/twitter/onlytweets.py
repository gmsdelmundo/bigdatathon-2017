#python3 


with open("processed_tweets.csv", "r") as fl:
	tweets = fl.read().split("\n")

tweets = [[ti[1:-1] for ti in t.split(",")] for t in tweets]

tweets = [t for t in tweets if len(t) >= 4 and t[3] == "tweet"]
print(len(tweets))
with open("tweets_only.csv", "w+") as fw:
	fw.write("\n".join([",".join(t) for t in tweets]))	
