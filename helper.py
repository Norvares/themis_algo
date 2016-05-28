import rethinkdb as r
from csvkit.convert.js import json2csv
from collections import OrderedDict
import StringIO, json

def dataToCSV():
    c = r.connect()
    cursor = r.db("themis").table("tolExperiment").run(c)
    data  = json.dumps([OrderedDict([
        ["clusters", item["config"]["tol"]],
        ["coefficient", item["evaluation"]["SilhouetteCoefficient"]]]) for item in cursor])
    converted = json2csv(StringIO.StringIO(data))
    print(converted)
