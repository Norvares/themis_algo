import json
import rethinkdb as r
import numpy as np
from sklearn.cluster import MeanShift
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler


global limit

def run():
    limit = 500
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

    # normalize dataset for easier parameter selection
    X = StandardScaler().fit_transform(X)

    # estimate bandwidth for mean shift
    bandwidth = cluster.estimate_bandwidth(X, quantile=0.3)

    # create clustering estimator
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)

    ms.fit(X)
    if hasattr(algorithm, 'labels_'):
        y_pred = ms.labels_.astype(np.int)
    else:
        y_pred = ms.predict(X)

    print(y_pred)

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
