import unicodedata
import sys
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import *

def stemmed (chunk):
    stemmed_word=[]
    stemmer = PorterStemmer()
    for word in chunk:
        stemmed_word.append(stemmer.stem(word))

    return stemmed_word

def removeStopwords(chunk):
    good = []
    for word in chunk:
        if word not in stopwords.words('english'):
            good.append(word)
    return good

def nlp(sentence):
    # Reducing the sentece to all lower case letters
    sentence = sentence.lower()

    # Tokenize the sentence
    tokens = nltk.word_tokenize(sentence)

    # Removing punctuation and unicode characters
    tokens = words = re.findall(r'\w+', sentence,flags = re.UNICODE | re.LOCALE)

    # Remove stopwords from the list
    important_words = []
    important_words = removeStopwords(tokens)

    # Performing porter stemming
    stu = []
    stu = stemmed(important_words)

    # Performing the final correction 
    final = []
    for word in stu:
        if word not in final:
            final.append(word)

    #remove numbers from the list
    final = [item for item in final if item.isalpha()]
    stu = [item for item in stu if item.isalpha()]

    '''
    stu contains duplicates
    final doesn't contain duplicates

    Duplicates are important when considering term frequencies and for weighting measures
    '''
    return stu