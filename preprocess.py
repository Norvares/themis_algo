import nltk
import re
import time

def onlyNounsAndNames(content):
    try:
        tokenized = nltk.word_tokenize(content)
        tagged = nltk.pos_tag(tokenized)
        words = ' '.join(word for word,tag in tagged if tag in ('NN', 'NNP') and word != 'Mr') 
        return words

    except Exception, e:
        print str(e)
