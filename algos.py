from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def kmeans(data, n_features, true_k, init, n_init, max_iter, tol, precompute_distance,
           verbose, random_state, copy_x, n_jobs):
    result = []
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data)

    model = KMeans(n_clusters=true_k, init=init, n_init=n_init, max_iter=max_iter, tol=tol,
                   precompute_distances=precompute_distance, verbose=verbose,
                   random_state=random_state, copy_x=copy_x, n_jobs=n_jobs)
    model.fit(X)
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        for ind in order_centroids[i, :n_features]:
            result.append(' %s' % terms[ind])
    return result


def kmeans_alt(data):
    result = []
    true_k = 5
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data)

    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit_predict(X)
    predictions = (model.predict(X))
    i = 0
    for i in range(len(predictions)):
        print(data[i])
        print()
        print(predictions[i])
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        for ind in order_centroids[i, :3]:
            result.append(' %s' % terms[ind])
    return result
