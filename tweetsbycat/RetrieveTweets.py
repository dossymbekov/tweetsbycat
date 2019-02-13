import tweepy
from tweepy import OAuthHandler
import time
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import subprocess
import os
from .settings import BACKEND_DIR

RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

def strip_emoji(text):
    return RE_EMOJI.sub(r'', text)

def load_api():
    consumer_key = "QU9kxhHKkdO00XjNeMDnyVIDX"
    consumer_secret = "LF96QFSvwWRA0b1i3bQyxvxOLe2juvnlKfUi0MStebRuqHMcko"
    access_key = "65542518-7FR8JkLYkgLBY43CgflDmiq8z8UuMhnML1KFAbfqA"
    access_secret = "OUu0qUm58Le7WAjsoRZ7E91P8joX7F2e5ynC5COlcsDkn"

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)

def preprocess(lines, s):
    text1 = lines.lower()   # do lower casing
    result = re.sub("http\S*", "", text1)  # remove the http links

    result1 = re.sub("RT \S*", "", result)
    reg2 = '[^\w\#\@\_]'
    out = re.compile(reg2).split(result1)
    result = [x for x in out if x not in s]   # stopwords removal
    return result

def stemming(lists):
    ps = PorterStemmer()
    temp = set()   # create a set to avoid duplicates
    for w in lists:
        temp.add(ps.stem(w))
    result = list(filter(None, list(temp)))
    return result  # return the list

def loadfeatures(df2, features):
    for index, row in df2.iterrows():
        key = row["feature"]
        value = row["feature_id"]
        features[key] = value

def classify():
    stoplist = stopwords.words('english')

    s = set(stoplist)

    #wd = "/Users/varunsharma/Downloads/TTDS DATA/"
    wd = BACKEND_DIR+"/outs/"
    #train_filepath = wd+"Tweets.cat.train"
    #df = pd.read_table(train_filepath, encoding="ISO-8859-1", header=None)

    test_filepath = wd + "valid.test"
    df1 = pd.read_table(test_filepath, encoding="ISO-8859-1", header=None)

    #pwd = "/Users/varunsharma/Downloads/TTDS DATA/"
    pwd = BACKEND_DIR+"/outs/"
    feature_filepath = pwd + "feats.dic"
    df2 = pd.read_table(feature_filepath, encoding="ISO-8859-1", header=None)

    #df.columns = ['tweet_id', 'text', 'classification']
    df1.columns = ['tweet_id', 'text', 'classification']
    df2.columns = ['feature_id', 'feature']

    features = {}

    classdict = {"Animals": 1,
                 "Agriculture": 2,
                 "Architecture": 3,
                 "Art and Photography": 4,
                 "Automobile": 5,
                 "Business & Finance": 6,
                 "Children": 7,
                 "Comics & Humor": 8,
                 "Computers and Electronics": 9,
                 "Food and Beverages": 10,
                 "Education": 11,
                 "Ethnic": 12,
                 "Fashion and Style": 13,
                 "Health and Fitness": 14,
                 "History": 15,
                 "Literature": 16,
                 "Medical": 17,
                 "Music": 18,
                 "Politics": 19,
                 "Psychology": 20,
                 "Religion": 21,
                 "Science and Nature": 22,
                 "Sports and Recreation": 23,
                 "TV and Movie": 24,
                 "Weather": 25}

    loadfeatures(df2, features)
    #with open("/Users/varunsharma/Downloads/TTDS DATA/feats_valid.test", mode="w", encoding="utf-8") as file:    
    with open(wd+"feats_valid.test", mode="w", encoding="utf-8") as file:
        for index, row in df1.iterrows():
            wordList = []
            text = row["text"]
            tokens = preprocess(str(text), s)
            words = stemming(tokens)

            temp = []
            for word in words:
                # Duplicate the words starting with hash
                if str.startswith(word, "#", 0) and len(word) > 1:
                    copy = word[1:]
                    wordList.append(copy)
                wordList.append(word)
            file.write(str(1) + "\t")

            for word in wordList:
                if word in features:
                    featureid = features.get(word)  # get the feature id
                    if featureid not in temp:
                        temp.append(featureid)

            temp.sort()
            for t in temp:
                file.write(str(t) + ":1" + " ")
            file.write("#" + str(123) + "\n")
    file.close()

def main(geo_code):
    api = load_api()
    query = "%20"
    language = "en"
    # Calling the user_timeline function with our parameters
    tweetSet = set([0])
    old_id = ""

    results = api.search(q=query, lang=language, geocode="39.8,-95.583068847656,2500km", count="1")
    #print(len(results))
    count = 0
    temp = 0

    wd = BACKEND_DIR+'/outs/'

    for tweet in results:
        old_id = tweet.id_str
    with open(wd+"valid.test", mode="w", encoding="utf-8") as file:

        for x in range(15):
            results = api.search(q=query, lang=language,  geocode=geo_code+",100km", since_id=old_id, count="100")
            for tweet in results:
                count += 1
                if tweet.id_str not in tweetSet:
                    if temp != 0:
                        file.write("\n")
                    file.write(tweet.id_str + "\t" + strip_emoji(tweet.text).strip().replace("\n","") + "\t"+"TEST")
                    temp += 1
                    tweetSet.add(int(tweet.id_str))
            if len(tweetSet) > 100:
                break
            time.sleep(2)
            #print(len(tweetSet))
            old_id = max(tweetSet)
    #print(len(tweetSet))
    classify()
    #subprocess.call(['/Users/varunsharma/Downloads/svm_multiclass/svm_multiclass_classify', '/Users/varunsharma/Downloads/TTDS DATA/feats_valid.test', '/Users/varunsharma/Downloads/svm_multiclass/model', '/Users/varunsharma/Downloads/svm_multiclass/pred3.out'])
    subprocess.call([BACKEND_DIR+'/svm_multiclass_linux64/svm_multiclass_classify', BACKEND_DIR+'/outs/feats_valid.test', BACKEND_DIR+'/svm_multiclass_linux64/model', BACKEND_DIR+'/svm_multiclass_linux64/pred3.out'])
    result_dict = readTopics()
    return result_dict

def readTopics():
    pwd = BACKEND_DIR+"/svm_multiclass_linux64/"
    pred_filepath = pwd + "pred3.out"
    df_p = pd.read_table(pred_filepath, header=None, sep=" ", usecols=[0])

    freq_ordered = df_p[0].value_counts()
    top5 = freq_ordered.head(5)
    total = top5.sum()
    top5df = top5.to_frame()

    top5_percent = ((top5df[0]/total)*100).to_frame()
    top5_dict = top5_percent.to_dict()[0]
    return top5_dict
def hello(strr):
    return str('Hello '+strr)
