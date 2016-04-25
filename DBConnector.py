import rethinkdb as r
import algos

c = r.connect()
cursor = r.db("themis").table("pages").run(c)
data = []
for document in cursor:
    databaseId = document['id']
    print(databaseId)
    data.append(str(document['content']).decode('unicode-escape'))
print(algos.kmeans(data))
#r.db("themis").table("pages").get(databaseId).update({"cluster": kmeansResult}).run(c)
