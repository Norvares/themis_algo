from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def kmeans(data):
    result = []
    true_k = 13
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data)

    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        for ind in order_centroids[i, :1]:
            result.append(' %s' % terms[ind])
    return result

