import nltk
import re
import time


var = raw_input("Please enter something: ")

example = 'Obama is fighting Putin'

def onlyNounsAndNames(content):
    try:
        tokenized = nltk.word_tokenize(content)
        tagged = nltk.pos_tag(tokenized)
        words = ' '.join(word for word,tag in tagged if tag in ('NN', 'NNP'))
        return words


    except Exception, e:
        print str(e)
