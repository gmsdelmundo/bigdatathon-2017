
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

sia = SIA()
res = sia.polarity_scores(txt)

print(res)