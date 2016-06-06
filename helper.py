import rethinkdb as r
from csvkit.convert.js import json2csv
from collections import OrderedDict
import StringIO, json
from gensim import corpora, matutils
from numpy import swapaxes

def dataToCSV():
    c = r.connect()
    cursor = r.db("themis").table("tolExperiment").run(c)
    data  = json.dumps([OrderedDict([
        ["clusters", item["config"]["tol"]],
        ["coefficient", item["evaluation"]["SilhouetteCoefficient"]]]) for item in cursor])
    converted = json2csv(StringIO.StringIO(data))
    print(converted)

def dataToSpaceVector(documents):
    # remove stopwords and tokenize
    stoplist = set('for a of the and to in mr mrs'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]

    # remove words that only appear once (this is considering all documents)
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]
    
    #create a dictionary consisting of each unique word in texts
    dictionary = corpora.Dictionary(texts)
    # this can be saved by uncommenting the next line
    # dictionary.save('/tmp/example.dict')
    
    # convert to SparseVector
    corpus = [dictionary.doc2bow(text) for text in texts]
    #print(corpus)    
    # this can be saved as well:
    # corpora.MmCorpus.serialize('/tmp/example.mm', vector)
   
    #matrix = matutils.corpus2csc(corpus)
    #print(matrix)
    numberOfCorpusFeatures = len(dictionary.keys())
    matrix = matutils.corpus2dense(corpus, num_terms=numberOfCorpusFeatures)
    print(matrix)
    print(matrix.shape)
    #x = matrix.swapaxes(0, 1) 
    #print(x.shape)
    return matrix
