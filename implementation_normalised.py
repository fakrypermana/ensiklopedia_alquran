from __future__ import division
import operator
import math
from collection import *
from nlp import *
from collections import OrderedDict
import collections


def getTfDoc(list_of_terms):
    for filename in list_of_filenames:
        data = getDocument(filename, sub_dir)
        # print('data : ', data)
        nlp_list = nlp(data)
        # print('data : ', nlp_list)
        for term in nlp_list:
            if term in list_of_terms:
                # if list_of_terms.has_key(term):
                if ids[filename] in list_of_terms[term]:
                    # if list_of_terms[term].has_key(ids[filename]):
                    list_of_terms[term][ids[filename]] = list_of_terms[term][ids[filename]] + 1
                else:
                    list_of_terms[term].update({ids[filename]: 1})
            else:
                list_of_terms.update({term: {ids[filename]: 1}})
    return list_of_terms


def getTfQuery(list_of_terms):
    for word in query:
        if word in list_of_query:
            # if list_of_terms[term].has_key(ids[filename]):
            list_of_terms[word] = list_of_terms[word] + 1
        else:
            list_of_terms.update({word: 1})
    return list_of_terms


def getWeightDocs(tfidf_scores, list_of_terms):
    docs_dict_freq = {}
    max_freq = {}
    for term, value in list_of_terms.items():
        # print('value item ', value)
        for docID, frequency in value.items():
            if docID in docs_dict_freq:
                docs_dict_freq[docID][term] = frequency
            else:
                docs_dict_freq.update({docID: {term: frequency}})
            for word, freq in docs_dict_freq[docID].items():
                if term in docs_dict_freq:
                    max_freq = max(docs_dict_freq[docID].items(), key=operator.itemgetter(1))[1]
                else:
                    max_freq.update({docID:  max(docs_dict_freq[docID].items(), key=operator.itemgetter(1))[1]})
            idf_value = math.log10(1 + float(total_documents / len(value)))
            normalised = frequency/max_freq[docID]
            # print('normalised ',frequency,'/',max_freq[docID])
            tfidf = idf_value * normalised
            if term in inverse_term_freq:
                # print('idf : ', inverse_term_freq)
                if docID in inverse_term_freq[term]:
                    # print('idf with doc id : ', inverse_term_freq[term][docID])
                    inverse_term_freq[term][docID] = idf_value
                    tfidf_scores[term][docID] = tfidf
                else:
                    inverse_term_freq[term].update({docID: idf_value})
                    tfidf_scores[term].update({docID: tfidf})
            else:
                inverse_term_freq.update({term: {docID: idf_value}})
                tfidf_scores.update({term: {docID: tfidf}})
    print('docs_dict_freq ', docs_dict_freq)
    print('max frequency ', max_freq)
    return tfidf_scores


def getWeightQuery(tfidf_scores, list_of_terms):
    for term, value in list_of_terms.items():
        # print('max frequency ', max_freq)
        max_freq = max(list_of_terms.items(), key=operator.itemgetter(1))[1]
        for docID, idf in inverse_term_freq[term].items():
            tfidf_scores.update({term: inverse_term_freq[term][docID] * max_freq})
    return tfidf_scores

def getDistanceDocs(tfidf, distance_dict):
    sum = 0
    docs_dict = {}
    for term, value in tfidf.items():
        for docID, weight in value.items():
            if docID in docs_dict:
                docs_dict[docID][term] = weight
            else:
                docs_dict.update({docID: {term: weight}})
    print('ini docID', docs_dict)
    for doc, words in docs_dict.items():
        for word, values in words.items():
            sum = sum + math.pow(float(values), 2)
        distance = math.sqrt(sum)
        distance_dict.update({doc: distance})
        sum = 0

    return distance_dict


def getDistanceQuery(tfidf):
    sum = 0
    for word, value in tfidf.items():
        sum = sum + math.pow(float(value), 2)
    distance = math.sqrt(sum)

    return distance


sub_dir = "document"
query = input("query : ")
print('')
# print('The query is "', query, '"')
query = nlp(query)

# initial dict
list_of_docs = {}
list_of_query = {}
total_documents = 0
inverse_term_freq = {}
tfidf_docs = {}
tfidf_query = {}
distance_query = 0
distance_docs = {}


# collect all the filenames
list_of_filenames = findall(sub_dir)
# print ('list file ',list_of_filenames)
total_documents = len(list_of_filenames)
# print ('total document ',len(list_of_filenames))

# assign them ids
ids = assignids(list_of_filenames)
# print('id : ', ids)

# calculate tf-idf (weight) document & query
list_of_docs.update(getTfDoc(list_of_docs))
list_of_query.update(getTfQuery(list_of_query))
print('list of term ', list_of_query, 'and ', list_of_docs)
tfidf_docs.update(getWeightDocs(tfidf_docs, list_of_docs))
tfidf_query.update(getWeightQuery(tfidf_query, list_of_query))
print('tfidf query', tfidf_query)
print('tfidf  doc', tfidf_docs)

# get distance query & document
distance_query = (getDistanceQuery(tfidf_query))
distance_docs.update(getDistanceDocs(tfidf_docs, distance_docs))
print('distance query ', distance_query)
print('distance docs ', distance_docs)

# get inner pproduct
inner_product = {}
sum_ip = 0
for word, value in tfidf_query.items():
    if word in tfidf_docs:
        for docID, values in tfidf_docs[word].items():
            sum_ip = sum_ip + float(value * values)
            inner_product.update({docID: sum_ip})
        sum_ip = 0
# for docID, ip in inner_product.items():
#     print(getFilenameById(docID, ids))
print('inner product ', inner_product)

# get similarity (tfidf)
similarity = {}
calculate = 0
for docID, value in inner_product.items():
    for doc, values in distance_docs.items():
        calculate = value / float(distance_query * distance_docs[doc])
        similarity.update({docID:calculate})
    calculate = 0

for docID, value in similarity.items():
    print('similarity ', docID, ' : ', similarity[docID])
    # if getFilenameById(docID,ids) in list_of_filenames:
    #     extract = getDocument(getFilenameById(docID,ids),sub_dir)
    # print('extracted text', extract)
