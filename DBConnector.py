import rethinkdb as r
import algos
import re
import argparse

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
global preprocessing
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


def runAlgo(tableName):
    table = 'pages2'
    db = 'themis'
    if(check_params()):
        c = r.connect()
        if(limit == 0):
            count_ = r.db(db).table(table).count().run(c)
            cursor = r.db(db).table(table).limit(count_).run(c)
        else:
            cursor = r.db(db).table(table).limit(limit).run(c)

        jsonResult = algos.kmeans(cursor, limit, n_features, true_k, init, n_init, max_iter, tol, precompute_distance, verbose, random_state, copy_x, n_jobs, preprocessing)
        r.db("themis").table(tableName).insert(jsonResult).run(c)

def check_params():
    # limit => integer und > 0
    if not isinstance(limit, int) or limit < 0:
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
    if not isinstance(tol, float) or tol > 1:
        print('tol invalid')
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

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-l', help = 'limit help', type = int, default = 100)
parser.add_argument('-nf', help = 'n_features help', type = int, default = 5)
parser.add_argument('-tk', help = 'true_k help', type = int, default = 8)
parser.add_argument('-i', help = 'init help', default = 'k-means++')
parser.add_argument('-ni', help = 'n_init help', type = int, default = 10)
parser.add_argument('-m', help = 'max_iter help', type = int, default = 300)
parser.add_argument('-t', help = 'tol help', type = float, default = 0.0001)
parser.add_argument('-p', help = 'precompute_distance help', type = bool, default = 'auto')
parser.add_argument('-v', help = 'verbose help', type = int, default = 0)
parser.add_argument('-r', help = 'random_state help', default = None)
parser.add_argument('-c', help = 'copy_x help', type = bool, default = True)
parser.add_argument('-nj', help = 'n_jobs help', default = 1)
parser.add_argument('-pp', help = 'preprocessing', default = 'None')
args = parser.parse_args()

limit = args.l
n_features = args.nf
true_k = args.tk
init = args.i
n_init = args.ni
max_iter = args.m
tol = args.t
precompute_distance = args.p
verbose = args.v
random_state = args.r
copy_x = args.c
n_jobs = args.nj
preprocessing = args.pp

runAlgo("results")
