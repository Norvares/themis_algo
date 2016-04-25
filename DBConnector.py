import rethinkdb as r
import algos

c = r.connect()
cursor = r.db("themis").table("pages").limit(1).run(c)
data = []
for document in cursor:
    databaseId = document['id']
    print(databaseId)
    kmeansResult = algos.kmeans(str(document['content']).decode('unicode-escape'))
    r.db("themis").table("pages").get(databaseId).update({"cluster": kmeansResult}).run(c)
