import re
import unicodedata
import argparse
import json
import rethinkdb as r
import numpy as np
from helper import dataToSpaceVector
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler, Normalizer

global limit

def run():
    table = 'pages'
    db = 'themis'
    if(check_params()):
        c = r.connect()
        if(limit == 0):
            count_ = r.db(db).table(table).count().run(c)
            cursor = r.db(db).table(table).limit(count_).run(c)
        else:
            cursor = r.db(db).table(table).limit(limit).run(c)

        jsonResult = meanshift(cursor)
        # TODO: create new result table!
        #r.db("themis").table("results_meanshift").insert(jsonResult).run(c)

def meanshift(cursor):
    data = []
    for document in cursor:
        line = (str(document['content']).decode('unicode-escape'))
        m = unicodedata.normalize('NFKD', line).encode('ascii', 'ignore')
        data.append(m)
   
    #vectorizer = TfidfVectorizer(stop_words='english')
    #X = vectorizer.fit_transform(data)
    #X = X.todense()
    X = dataToSpaceVector(data)
    #countVectorized = CountVectorizer().fit_transform(data)    
    #tfidfVectorized = TfidfTransformer().fit_transform(countVectorized)
    #tfidfArray = tfidfVectorized.toarray()
    #X = StandardScaler().fit_transform(X)
    #X = tfidfVectorized
    #X = np.array(Vector)

    # estimate bandwidth for mean shift
    bandwidth = estimate_bandwidth(X, quantile=0.3)

    # create clustering estimator
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)

    labels_unique = np.unique(ms.labels_)
    n_clusters_ = len(labels_unique)
    print("number of estimated clusters : %d" % n_clusters_)
    print(labels_unique)
    print('labels: die Werte sind < 0, und werden auf 0 gerundet')
    print(ms.labels_)

    return n_clusters_


def check_params():
    # limit => integer und > 0
    if not isinstance(limit, int) or limit < 0:
        print('limit invalid')
        return False
    return True


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-l', help = 'limit help', type = int, default = 100)
args = parser.parse_args()

limit = args.l
run()
