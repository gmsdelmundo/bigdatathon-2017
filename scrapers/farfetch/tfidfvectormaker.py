from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.externals import joblib

with open("kv-data", "r") as fl:
    dataset = [f.split(",") for f in fl.read().split("\n")]

#get descriptions
print(dataset[0][5])
descriptions = [t[5] for t in dataset if len(t) > 6]
print(descriptions[0])
vectorizer = TfidfVectorizer(stop_words='english')
vecs = vectorizer.fit_transform(descriptions)
joblib.dump(vectorizer, "productdescriptionvector.pkl")

