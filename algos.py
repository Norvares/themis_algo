from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics
import rethinkdb as r
import datetime
import json
import preprocess


def kmeans(cursor, limit, n_features, true_k, init, n_init, max_iter, tol, precompute_distance,
           verbose, random_state, copy_x, n_jobs, preprocessing, mindf, maxdf):
#    mindf = 0.0
#    maxdf = 0.8

    data = []
    ids = []
    titles = []
    uris = []

    if (preprocessing == "lemmatizer"):
        for document in cursor:
            text_string = (str(document['content']).decode('unicode-escape'))
            words = preprocess.lemmatizer(text_string)
            data.append(words)
            ids.append(document['id'])
            titles.append(document['title'])
            uris.append(document['url'])
    elif (preprocessing == "stemmer"):
        for document in cursor:
            text_string = (str(document['content']).decode('unicode-escape'))
            words = preprocess.stemmer(text_string)
            data.append(words)
            ids.append(document['id'])
            titles.append(document['title'])
            uris.append(document['url'])
    elif (preprocessing == "onlyNounsAndNames"):
        for document in cursor:
            text_string = (str(document['content']).decode('unicode-escape'))
            words = preprocess.onlyNounsAndNames(text_string)
            data.append(words)
            ids.append(document['id'])
            titles.append(document['title'])
            uris.append(document['url'])
    elif (preprocessing == "NounsLemma"):
        for document in cursor:
            text_string = (str(document['content']).decode('unicode-escape'))
            words = preprocess.onlyNounsAndNames(text_string)
            words = preprocess.lemmatizer(words)
            data.append(words)
            ids.append(document['id'])
            titles.append(document['title'])
            uris.append(document['url'])
    elif (preprocessing == "NounsStemmer"):
        for document in cursor:
            text_string = (str(document['content']).decode('unicode-escape'))
            words = preprocess.onlyNounsAndNames(text_string)
            words = preprocess.stemmer(words)
            data.append(words)
            ids.append(document['id'])
            titles.append(document['title'])
            uris.append(document['url'])
    else:
        preprocessing = None
        for document in cursor:
            text_string = (str(document['content']).decode('unicode-escape'))
            data.append(text_string)
            ids.append(document['id'])
            titles.append(document['title'])
            uris.append(document['url'])

    result = []
    vectorizer = TfidfVectorizer(stop_words='english', max_features=n_features)
    X = vectorizer.fit_transform(data)

    model = KMeans(n_clusters=true_k, init=init, n_init=n_init, max_iter=max_iter, tol=tol,
                   precompute_distances=precompute_distance, verbose=verbose,
                   random_state=random_state, copy_x=copy_x, n_jobs=n_jobs)

    # one result json per run
    jsn = {}    # result cluster json with params, features and docs
    jsn['preprocess'] = preprocessing
    jsn['createdAt'] = str(datetime.datetime.now())    # set ID
    params_conf = model.get_params()
    params_conf['limit'] = limit
    params_conf['n_features'] = n_features
    jsn['config'] = params_conf  # set CONFIG/ PARAMS
    jsn['data'] = []    # init DATA Array

    model.fit_predict(X)
    labels = model.labels_
    score = metrics.silhouette_score(X, labels, metric='euclidean')
    evaluationContent = {}
    evaluationContent['SilhouetteCoefficient'] = score
    jsn['evaluation'] = evaluationContent
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
            print(' %s' % terms[ind])
            ary_tmp_feat.append(' %s' % terms[ind])  # append features
            result.append(' %s' % terms[ind])
        print('')
        jsn_tmp['features'] = ary_tmp_feat   # set array of features
        jsn_tmp['articles'] = predict_map[i]  # set array of docs
        jsn['data'].append(jsn_tmp) # write jsn_tmp to jsn['data']

    idf = vectorizer.idf_
    print dict(zip(vectorizer.get_feature_names(), idf))
    return (jsn)
