import algos
import rethinkdb as r

c = r.connect()
i = 0
while (i < 0.002):
    cursor = r.db("themis").table("pages").limit(1000).run(c)
    jsonResult = algos.kmeans(cursor, 1000, 20, 250, 'k-means++', 10, 1000, i, 'auto', 0, None, True, 1, None)
    r.db("themis").table("tolExperiment").insert(jsonResult).run(c)
    i = i+0.00002
