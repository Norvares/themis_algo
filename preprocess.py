import nltk
import re
import time


var = raw_input("Please enter something: ")

exampleArray = [var]

def onlyNounsAndNames():
    try:
        for item in exampleArray:
            tokenized = nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokenized)
            words = ' '.join(word for word,tag in tagged if tag in ('NN', 'NNP'))
            print words


    except Exception, e:
        print str(e)

processLanguage()
