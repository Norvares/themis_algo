import nltk
import re
import time


var = raw_input("Please enter something: ")

exampleArray = [var]

def processLanguage():
    try:
        for item in exampleArray:
            tokenized = nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokenized)
            print [(word, tag) for word, tag in tagged if tag in ('NN')]

            time.sleep(555)


    except Exception, e:
        print str(e)

processLanguage()
