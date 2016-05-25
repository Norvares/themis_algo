import algos
import rethinkdb as r

i = 2
while (i < 1000):
    cursor = r.db("themis").table("pages").limit(limit).run(c)
    jsonResult = algos.kmeans(cursor, 1000, 20, i, 'k-means++', 10, 1000, 0.0001, 'auto', 0, None, true, 1, None)
    r.db("themis").table("trueKExperiment").insert(jsonResult).run(c)
    i = i+1
