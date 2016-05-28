import rethinkdb as r
from csvkit.convert.js import json2csv

def dataToCSV():
    c = r.connect()
    output = r.db("db").table("trueKExperiment") \
    .group(r.row["config"]["n_cluster"]) \
    .ungroup().merge(r.row["evaluation"]["SilhouetteCoefficient"]).run(conn)
    print (output)
