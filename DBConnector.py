import rethinkdb as rdb
from algos import kmeans
import h5py

def storeInFile(limit):
    dataFile = h5py.File('data.hdf5','r')
    connection = rdb.connect()
    cursor = rdb.db("themis").table("pages").limit(limit).run(connection)
    dset = dataFile.create_dataset("test", (1,))
    dir(dset)
    i = 0
    for document in cursor:
        id = document['id']
        i=i+1
        print(str(i) + " " + id)
        dset[i]=(str(document['content']).decode('unicode-escape'))

#r.db("themis").table("pages").get(databaseId).update({"cluster": kmeansResult}).run(c)
