from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

txt = "The house was huge"
sia = SIA()
res = sia.polarity_scores(txt)

print(res)