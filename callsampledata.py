import rethinkdb as r

c = r.connect()
data = []
cursor = r.db("themis").table("pages").limit(1).run(c)
for document in cursor:
    print("new run")
    data.append(str(document['content']).decode('unicode-escape'))
    print(document['id'])
print(data)
