import rethinkdb as r
import algos
import re


global limit
global data
global n_features
global true_k
global init
global n_init
global max_iter
global tol
global precompute_distance
global verbose
global random_state
global copy_x
global n_jobs
'''
Parameter Liste:
limit = max. Anzahl zu ladener Datensaetze
data = dataset
n_features = Anzahl der Woerter-Features je Cluster

true_k (default: 8)
init (default: 'k-means++')
n_init (default: 10)
max_iter (default: 300)
tol (default: 0.0001)
precompute_distance (default: 'auto')
verbose (default: 0)
random_state (default: None)
copy_x (default: True)
n_jobs (default: 1)
'''


def runAlgo(limit_, data_, n_features_, true_k_, init_, n_init_, max_iter_, tol_, precompute_distance_,
            verbose_, random_state_, copy_x_, n_jobs_):
    limit = limit_
    data = data_
    n_features = n_features_
    true_k = true_k_
    init = init_
    n_init = n_init_
    max_iter = max_iter_
    tol = tol_
    precompute_distance = precompute_distance_
    verbose = verbose_
    random_state = random_state_
    copy_x = copy_x_
    n_jobs = n_jobs_

    if(check_params()):
        c = r.connect()
        cursor = r.db("themis").table("pages").limit(limit).run(c)
        i = 0
        data = []
        for document in cursor:
            databaseId = document['id']
            i=i+1
            print(str(i) + " " + databaseId)
            data.append(str(document['content']).decode('unicode-escape'))
        print(algos.kmeans(data, n_features, true_k, init, n_init, max_iter, tol, precompute_distance, verbose, random_state, copy_x, n_jobs))
        #r.db("themis").table("pages").get(databaseId).update({"cluster": kmeansResult}).run(c)


def runAlgo_alt(limit):
    c = r.connect()
    if (limit == 0):
        cursor = r.db("themis").table("pages").run(c)
    else:
        cursor = r.db("themis").table("pages").limit(limit).run(c)
    i = 0
    data = []
    ids = []
    for document in cursor:
        ids.append(document['id'])
        data.append(str(document['content']).decode('unicode-escape'))
    print(algos.kmeans_alt(data, ids))
    # r.db("themis").table("pages").get(databaseId).update({"cluster": kmeansResult}).run(c)


def check_params():
    # limit => integer und > 0
    if not isinstance(limit, int) or limit <= 0:
        print('limit invalid')
        return False

    # n_feature => integer und > 0
    if not isinstance(n_features, int) or n_features <= 0:
        print('n_feature invalid')
        return False

    # true_k => integer und > 0
    if not isinstance(true_k, int) or true_k <= 0:
        print('true_k invalid')
        return False

    # n_init => integer und > 0
    if not isinstance(n_init, int) or n_init <= 0:
        print('n_init invalid')
        return False

    # max_iter => integer und > 0
    if not isinstance(max_iter, int) or max_iter <= 0:
        print('max_iter invalid')
        return False

    # tol => float und <= 1
    if not isinstance(tol, float) or max_iter > 1:
        print('tol invalid')
        return False

    # precompute_distance => bool
    if not isinstance(precompute_distance, bool):
        print('precompute_distance invalid')
        return False

    # verbose => int
    if not isinstance(verbose, int):
        print('verbose invalid')
        return False

    # copy_x => bool
    if not isinstance(copy_x, bool):
        print('copy_x invalid')
        return False

    return True
