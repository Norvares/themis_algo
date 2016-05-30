import re
import argparse
import json
import rethinkdb as r
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
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

        jsonResult = affinityPropagation(cursor)
        # TODO: create new result table!
        #r.db("themis").table("results_af").insert(jsonResult).run(c)

def affinityPropagation(cursor):
    data = []
    for document in cursor:
        data.append(str(document['content']).decode('unicode-escape'))

    X = StandardScaler().fit_transform(data)

    # Compute Affinity Propagation
    af = AffinityPropagation(preference=-50).fit(X)
    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_

    n_clusters_ = len(cluster_centers_indices)

    print('Estimated number of clusters: %d' % n_clusters_)
#    print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
#    print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
#    print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
#    print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(labels_true, labels))
#    print("Adjusted Mutual Information: %0.3f" % metrics.adjusted_mutual_info_score(labels_true, labels))
#    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels, metric='sqeuclidean'))

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
