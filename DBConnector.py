import rethinkdb as rdb
from algos import kmeans
import h5py


def storeInFile(limit):
    dataFile = h5py.File('data.hdf5','r')
    connection = rdb.connect()
    cursor = rdb.db("themis").table("pages").limit(limit).run(connection)
    dset = dataFile.create_dataset("test", (1,))
    for document in cursor:
        dset.append(str(document['content']).decode('unicode-escape'))

#i = 0
#data = []
#for document in cursor:
#    databaseId = document['id']
#    i=i+1
#    print(str(i) + " " + databaseId)
#    data.append(str(document['content']).decode('unicode-escape'))
#print(kmeans(data))
#r.db("themis").table("pages").get(databaseId).update({"cluster": kmeansResult}).run(c)
