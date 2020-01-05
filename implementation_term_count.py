from __future__ import division

import csv
import operator
import math
from collection import *
from nlp import *
from collections import OrderedDict
import collections
import textwrap

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

def getDistanceDocs(list_of_terms, distance_dict):
    sum = 0
    for term, value in list_of_terms.items():
        for docID, freq in value.items():
            if docID in freq_docs_dict:
                freq_docs_dict[docID][term] = freq
            else:
                freq_docs_dict.update({docID: {term: freq}})
    # print('ini freq docID', freq_docs_dict)
    for docID, value in freq_docs_dict.items():
        # print('value item ', value)
        for term, frequency in value.items():
            sum = sum + math.pow(float(frequency), 2)
        distance = math.sqrt(sum)
        distance_dict.update({docID: distance})
        sum = 0
    return distance_dict


def getDistanceQuery(list_of_term):
    sum = 0
    for word, value in list_of_term.items():
        sum = sum + math.pow(float(value), 2)
    distance = math.sqrt(sum)

    return distance


sub_dir = "data"
query = input("query : ")
print('')
# print('The query is "', query, '"')
query = nlp(query)

'''initial dict'''
list_of_docs = {}
list_of_query = {}
total_documents = 0
distance_query = 0
distance_docs = {}
freq_docs_dict = {}

'''collect all the filenames'''
list_of_filenames = findall(sub_dir)
# print ('list file ',list_of_filenames)
total_documents = len(list_of_filenames)
# print ('total document ',len(list_of_filenames))

'''assign them ids'''
ids = assignids(list_of_filenames)
# print('id : ', ids)

'''frequency document & query'''
list_of_docs.update(getTfDoc(list_of_docs))
list_of_query.update(getTfQuery(list_of_query))
# print('list of term ', list_of_query, 'and ', list_of_docs)

'''get distance query & document'''
distance_query = (getDistanceQuery(list_of_query))
distance_docs.update(getDistanceDocs(list_of_docs, distance_docs))
print('===================== CALCULATION =====================')
print('distance query ', distance_query)
print('distance docs ', distance_docs)

# get inner product
inner_product = {}
sum_ip = 0
for docID, values in freq_docs_dict.items():
    for word, value in list_of_query.items():
        if word in values:
            # print('bangsul ', docs_dict[docID])
            # print('ini value ', values[word])
            sum_ip = sum_ip + float(value * values[word])
        inner_product.update({docID: sum_ip})
    # print('hilih kintil ',sum_ip)
    sum_ip = 0
# for docID, ip in inner_product.items():
#     print(getFilenameById(docID, ids))
for docID, score in inner_product.items():
    if score > 0 :
        print('dot product ',getFilenameById(docID,ids),' ', inner_product[docID])
print("=========================================================\n")

# get similarity
similarity = {}
calculate = 0
for docID, value in inner_product.items():
    for doc, values in distance_docs.items():
        if docID == doc:
            calculate = value / float(distance_query * distance_docs[doc])
            similarity.update({getFilenameById(docID, ids):calculate})
    calculate = 0

sorted_similarity = OrderedDict(sorted(similarity.items(), key=lambda x: x[1], reverse=True))
print('')
print("========= Displaying results in relevance order =========")
for docID, score in sorted_similarity.items():
    if score > 0:
        print(docID, " : ", similarity[docID])

try:
    with open('result-tc.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in similarity.items():
            writer.writerow([key, value])
except IOError:
    print('I/O error')

extract = []
for doc, score in sorted_similarity.items():
    extract.append(getDocument(doc, sub_dir))
print("========================================== EXTRACTED TEXT ==========================================")
print('\n', textwrap.fill(extract[0], 100))
print("====================================================================================================")
    # if getFilenameById(docID,ids) in list_of_filenames:
    #     extract = getDocument(getFilenameById(docID,ids),sub_dir)
    # print('extracted text', extract)
