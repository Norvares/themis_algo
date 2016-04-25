import rethinkdb as r
import algos

c = r.connect()
cursor = r.db("themis").table("pages").limit(5000).run(c)
i = 0
data = []
for document in cursor:
    databaseId = document['id']
    i=i+1
    print(str(i) + " " + databaseId)
    data.append(str(document['content']).decode('unicode-escape'))
print(algos.kmeans(data))
#r.db("themis").table("pages").get(databaseId).update({"cluster": kmeansResult}).run(c)
