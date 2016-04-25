import rethinkdb as r
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def algo():
    c = r.connect()
    cursor = r.db("themis").table("pages").limit(1).run(c)
    result = []
    data = []
    for document in cursor:
        data.append(str(document['content']).decode('unicode-escape'))
    true_k = 1
    vectorizer = TfidfVectorizer(stop_words='english')
    print(data)
    X = vectorizer.fit_transform(data)

    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        for ind in order_centroids[i, :10]:
            result.append(' %s' % terms[ind])
    print (result)

