from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.externals import joblib
###Training data
#read both good and bad files
# with open("goodCritiques.txt", "r", encoding='latin1') as fl:
#     good = fl.read().split("|")
#     good = [(g, 0) for g in good]
# with open("badCritiques.txt", "r", encoding='latin1') as fl:
#     bad = fl.read().split("|")
#     bad = [(b, 1) for b in bad]
# alldocs = good + bad
# X_train, X_test, y_train, y_test = train_test_split([t[0] for t in alldocs], [t[1] for t in alldocs], test_size=0.25)
# #make the vector
# vectorizer = TfidfVectorizer(stop_words='english')
# vecs = vectorizer.fit_transform(X_train)
# joblib.dump(vectorizer, "vectorizer.pkl")
# ## training the model
# clf = SGDClassifier()
# clf.fit(vecs, y_train)
#
#
# test_vecs = vectorizer.transform(X_test)
#
# score = clf.score(test_vecs, y_test)
#
# print(score)
#
# joblib.dump(clf, "spamclassifier.pkl")

clf = joblib.load("spamclassifier.pkl")
vecs = joblib.load("vectorizer.pkl")
badtest = "where is the booty"
goodtest = "I would like to congratulate you on making this work of art as somewhat curious as it is.The concept you have actualized is truly incredible. It is obvious to me that you kept your nose to the grind-stone with your complete capacity of abilities. The line of this picture is decisively exact for the feeling that I contemplate you are trying to create, but now that I think about it this observation is likely superfluous. However, I sense that your implementation of fore-shortening could have been done better as I sense that it doesn't duplicate the quality obvious in the rest of the art work. In the end I would like to illuminate that it has been a pleasure to jot down this assessment for you and I feel it will empower you to up the level of your excellent piece."

badtest = vecs.transform([badtest])
goodtest = vecs.transform([goodtest])

print(clf.predict(badtest))
print(clf.predict(goodtest))