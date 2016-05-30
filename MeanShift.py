import re
import argparse
import json
import rethinkdb as r
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler


global limit

def run():
    limit = 10
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
        data.append(str(document['content']).decode('unicode-escape'))

    vectorizer = CountVectorizer(min_df=1)
    X = vectorizer.fit_transform(data)
    X = X.toarray()

   # normalize dataset for easier parameter selection
    X = StandardScaler().fit_transform(X)

    # estimate bandwidth for mean shift
    bandwidth = estimate_bandwidth(X, quantile=0.9)

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
