from __future__ import division

import math
from collections import OrderedDict

from collection import *
from nlp import *


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
    for term, value in list_of_terms.items():
        # print('value item ', value)
        for docID, frequency in value.items():
            # print('docID value item ',value)
            # print('inside ', total_documents,'/',len(value))
            idf_value = math.log10(1 + float(total_documents / len(value)))
            tfidf = idf_value * frequency
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
    return tfidf_scores


def getWeightQuery(tfidf_scores, list_of_terms):
    for term, value in list_of_terms.items():
        for docID, idf in inverse_term_freq[term].items():
            tfidf_scores.update({term: inverse_term_freq[term][docID] * value})
    return tfidf_scores


def getDistanceDocs(tfidf, distance_dict):
    sum = 0
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
docs_dict = {}

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
for docID, values in docs_dict.items():
    for word, value in tfidf_query.items():
        if word in values:
            # print('bangsul ', docs_dict[docID])
            # print('ini value ', values[word])
            sum_ip = sum_ip + float(value * values[word])
        inner_product.update({docID: sum_ip})
    # print('hilih kintil ',sum_ip)
    sum_ip = 0
# for docID, ip in inner_product.items():
#     print(getFilenameById(docID, ids))
print('inner product ', inner_product)

# get similarity (tfidf)
similarity = {}
for docID, value in inner_product.items():
    for doc, values in distance_docs.items():
        calculate = value / float(distance_query * distance_docs[docID])
        # print('perhitungan ',value,'/','float(',distance_query,'*',distance_docs[docID],')')
        similarity.update({docID: calculate})
    calculate = 0

sorted_similarity = OrderedDict(sorted(similarity.items(), key=lambda x: x[1], reverse=True))
print('')
print("Displaying results in relevance order")
for docID, score in sorted_similarity.items():
    print(getFilenameById(docID, ids), " : ", similarity[docID])

# if getFilenameById(docID,ids) in list_of_filenames:
#     extract = getDocument(getFilenameById(docID,ids),sub_dir)
# print('extracted text', extract)
