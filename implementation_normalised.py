from __future__ import division

import csv
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

def getNormalisedTermDocs(list_of_terms,normalised):
    total_term = 0
    for terms, value in list_of_terms.items():
        for docID, freq in value.items():
            if docID in freq_docs_dict:
                freq_docs_dict[docID][terms] = freq
            else:
                freq_docs_dict.update({docID: {terms: freq}})
    for docId, word in freq_docs_dict.items():
        for term, freq in word.items():
            total_term+=freq
            docs_total_term.update({docId : total_term})
        total_term = 0
    for term, value in list_of_terms.items():
        for docID, freq in value.items():
            if term in normalised:
                # if list_of_terms.has_key(term):
                normalised[term][docID] = freq/docs_total_term[docID]
            else:
                normalised.update({term:{docID:freq/docs_total_term[docID]}})
    print('total term ', docs_total_term)
    return normalised


def getTfQuery(list_of_terms):
    for word in query:
        if word in list_of_query:
            # if list_of_terms[term].has_key(ids[filename]):
            list_of_terms[word] = list_of_terms[word] + 1
        else:
            list_of_terms.update({word: 1})
    return list_of_terms

def getNormalisedQuery(list_of_terms,normalised):
    for word, value in list_of_terms.items():
        normalised.update({word : value/len(list_of_terms)})
    return normalised


def getWeightDocs(tfidf_scores, normalised):
    for term, value in normalised.items():
        # print('value item ', value)
        for docID, frequency in value.items():
            # print('docID value item ',value)
            # print('inside ', total_documents,'/',len(value))
            idf_value = math.log10(float(total_documents / len(value)))
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
        # print('max frequency ', max_freq)
        max_freq = max(list_of_terms.items(), key=operator.itemgetter(1))[1]
        for docID, idf in inverse_term_freq[term].items():
            tfidf_scores.update({term: inverse_term_freq[term][docID] * max_freq})
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
        # print('ini sumiati ',sum)
        sum = sum + math.pow(float(value), 2)
        # print('ini sumiati uplot ', sum)
    distance = math.sqrt(sum)

    return distance


sub_dir = "document"
query = input("query : ")
print('')
# print('The query is "', query, '"')
query = nlp(query)

# initial dictionary
list_of_docs = {}
list_of_query = {}
list_of_term_normlised = {}
total_documents = 0
inverse_term_freq = {}
tfidf_docs = {}
tfidf_query = {}
distance_query = 0
distance_docs = {}
docs_dict = {}
normalised_query = {}
normalised_docs = {}
docs_total_term = {}
freq_docs_dict = {}

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
normalised_docs.update(getNormalisedTermDocs(list_of_docs,normalised_docs))
normalised_query.update(getNormalisedQuery(list_of_query,normalised_query))
print('normalised ',normalised_query,'and',normalised_docs)
tfidf_docs.update(getWeightDocs(tfidf_docs, normalised_docs))
tfidf_query.update(getWeightQuery(tfidf_query, normalised_query))
print('freq kemunculan kata ', freq_docs_dict)
print('idf doc', inverse_term_freq)
print('tfidf query', tfidf_query)
print('tfidf  doc', tfidf_docs)

# get distance query & document
distance_query = (getDistanceQuery(tfidf_query))
distance_docs.update(getDistanceDocs(tfidf_docs, distance_docs))
print('distance query ', distance_query)
print('distance docs ', distance_docs)

# get inner product
inner_product = {}
sum_ip = 0
for docID, value in docs_dict.items():
    for word, values in tfidf_query.items():
        if word in value:
            # print('samsudin ', sum_ip)
            # print('value bangsul ',word,' ',docID,' ', value[word], '*', values)
            sum_ip = sum_ip + float(value[word] * values)
    # print('samsudin uplot', sum_ip)
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
        if docID == doc:
            # print('calculate ',value,'/',distance_query,'*',distance_docs[doc])
            calculate = value / float(distance_query * distance_docs[doc])
            # print('ini calculate ', calculate)
            similarity.update({getFilenameById(docID, ids):calculate})
    calculate = 0

sorted_similarity = OrderedDict(sorted(similarity.items(), key=lambda x: x[1], reverse=True))
print('')
print("Displaying results in relevance order")
for docID, score in sorted_similarity.items():
    print('docID',docID,' ',getFilenameById(docID, ids), " : ", similarity[docID])

try:
    with open('result-nf.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in similarity.items():
            writer.writerow([key, value])
except IOError:
    print('I/O error')
    # if getFilenameById(docID,ids) in list_of_filenames:
    #     extract = getDocument(getFilenameById(docID,ids),sub_dir)
    # print('extracted text', extract)
