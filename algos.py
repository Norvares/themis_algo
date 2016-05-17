from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import rethinkdb as r
import datetime
import json


def kmeans(cursor, limit, n_features, true_k, init, n_init, max_iter, tol, precompute_distance,
           verbose, random_state, copy_x, n_jobs):
    data = []
    ids = []
    titles = []
    uris = []
    for document in cursor:
        data.append(str(document['content']).decode('unicode-escape'))
        ids.append(document['id'])
        titles.append(document['title'])
        uris.append(document['uri'])

    result = []
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data)

    model = KMeans(n_clusters=true_k, init=init, n_init=n_init, max_iter=max_iter, tol=tol,
                   precompute_distances=precompute_distance, verbose=verbose,
                   random_state=random_state, copy_x=copy_x, n_jobs=n_jobs)

    # one result json per run
    jsn = {}    # result cluster json with params, features and docs
    jsn['id'] = str(datetime.datetime.now())    # set ID
    params_conf = model.get_params()
    params_conf['limit'] = limit
    jsn['config'] = params_conf  # set CONFIG/ PARAMS
    jsn['data'] = []    # init DATA Array

    model.fit_predict(X)
    predictions = (model.predict(X))
    #predict_map = {}    # init dict, collect all articleIds per cluster
    predict_map = {}    # init dict, collect all article details per cluster

    i = 0
    for i in range(len(predictions)):
        if(predict_map.has_key(predictions[i])):
            detail_jsn = {}
            detail_jsn['articleId'] = ids[i]
            detail_jsn['title'] = titles[i]
            detail_jsn['uri'] = uris[i]
            predict_map[predictions[i]].append(detail_jsn)
        else:
            predict_map[predictions[i]] = []    # create new array for articleIds

    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        jsn_tmp = {}    # temp json for each cluster
        ary_tmp_feat = []   # init temp array of features
        for ind in order_centroids[i, :n_features]:
            ary_tmp_feat.append(' %s' % terms[ind])  # append features
            result.append(' %s' % terms[ind])
        jsn_tmp['features'] = ary_tmp_feat   # set array of features
        jsn_tmp['articles'] = predict_map[i]  # set array of docs
        jsn['data'].append(jsn_tmp) # write jsn_tmp to jsn['data']
    return (jsn)
