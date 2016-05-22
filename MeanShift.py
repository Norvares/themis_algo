import re
import argparse
import json
import rethinkdb as r
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler


global limit

def run():
    limit = 10
    table = 'pagesNew2'
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

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data)
    Y = X.toarray()
    print(Y)
    print('--')
    print(X)

    # normalize dataset for easier parameter selection
    Y = StandardScaler().fit_transform(Y)

    # estimate bandwidth for mean shift
    bandwidth = estimate_bandwidth(Y, quantile=0.2)

    # create clustering estimator
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)

    foo = ms.fit_predict(Y)
    print(foo)
 
    if hasattr(ms, 'labels_'):
        y_pred = ms.labels_.astype(np.int)
    else:
        y_pred = ms.predict(Y)

#    cluster_centers = ms.cluster_centers_
#    print(cluster_centers)
    labels_unique = np.unique(ms.labels_)
    n_clusters_ = len(labels_unique)
    print("number of estimated clusters : %d" % n_clusters_)

    print(y_pred)
    return True


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
