from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.decomposition import PCA
import rethinkdb as r
import datetime
import json
import preprocess
import random


# for visualization
import time
import numpy as np
import matplotlib.pyplot as plt


def kmeans(cursor, limit, n_features, true_k, init, n_init, max_iter, tol, precompute_distance,
           verbose, random_state, copy_x, n_jobs, preprocessing, visualization):

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
    elif (preprocessing == "topten"):
        for document in cursor:
            text_string = (str(document['content']).decode('unicode-escape'))
	    words = preprocess.onlyNounsAndNames(text_string)
            words = preprocess.topTen(words)
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

    reduced_data = PCA(n_components=2).fit_transform(X.toarray())

    model.fit_predict(reduced_data)
    labels = model.labels_
    score = metrics.silhouette_score(reduced_data, labels, metric='euclidean')
    evaluationContent = {}
    evaluationContent['SilhouetteCoefficient'] = score
    jsn['evaluation'] = evaluationContent
    predictions = (model.predict(reduced_data))
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

    if visualization:
        t0 = time.time()
        t_batch = time.time() - t0
        k_means_labels = model.labels_
        k_means_cluster_centers = model.cluster_centers_
        k_means_labels_unique = np.unique(k_means_labels)

        ##############################################################################
        # Plot result
        fig = plt.figure(figsize=(8, 8))
        fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)

        # Generate colors
        #colors = ['#4EACC5', '#FF9C34', '#4E9A06', '#468a05', '#a6cc82']
        colors = []
        for i in range(true_k):
            r = lambda: random.randint(0,255)
            colors.append('#%02X%02X%02X' % (r(),r(),r()))

        # KMeans
        ax = fig.add_subplot(1, 3, 1)
        for k, col in zip(range(true_k), colors):
            my_members = k_means_labels == k
            cluster_center = k_means_cluster_centers[k]
            ax.plot(reduced_data[my_members, 0], reduced_data[my_members, 1], 'w',
                    markerfacecolor=col, marker='.')
            ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                    markeredgecolor='k', markersize=6)
        ax.set_title('KMeans')
        ax.set_xticks(())
        ax.set_yticks(())
        plt.text(-3.5, 1.8,  'train time: %.2fs\ninertia: %f' % (
            t_batch, model.inertia_))

        plt.show()

    return (jsn)
