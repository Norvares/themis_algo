import nltk
import re
import time
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer


def onlyNounsAndNames(content):
    stoplist = set('mr mrs mr. mrs. ms ms.'.split())
    text = ' '.join(word for word in content.lower().split() if word not in stoplist)
    tokenized = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokenized)
    words = ' '.join(word for word,tag in tagged if tag in ('NN', 'NNP') and word != 'mr')
    return words
    
def lemmatizer(content):
    try:
        wordnet_lemmatizer = WordNetLemmatizer()
        tokenized = nltk.word_tokenize(content)
        tagged = nltk.pos_tag(tokenized)
        words = ' '.join(wordnet_lemmatizer.lemmatize(word, 'v') for word in content.split())
        return words
    except Exception, e:
        print("lemmatizer failed")

def stemmer(content):
    try:
        stemmer = SnowballStemmer("english")
        words = ' '.join([stemmer.stem(word) for word in content.split()])
        return words
    except Exception, e:
        print("stemmer failed")

def topTen(document):
    stoplist = set('for a of the and to in mr mrs mr. mrs. ms.'.split())
    text = [word for word in document.lower().split() if word not in stoplist]
    count = defaultdict(int)
    for word in text:
	count[word] += 1
    sort = OrderedDict()
    for key, value in sorted(count.iteritems(), key=lambda (k,v): (v,k)):
	sort[key] = value
    topTen = Counter(sort).most_common(10)
    words = ' '.join(key for key,value in topTen)
    return words

