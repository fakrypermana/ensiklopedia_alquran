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

def getDistanceDocs(list_of_terms, distance_dict):
    sum = 0
    for term, value in list_of_terms.items():
        # print('value item ', value)
        for docID, frequency in value.items():
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


sub_dir = "document"
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
print('distance query ', distance_query)
print('distance docs ', distance_docs)

# get inner product
inner_product = {}
sum_ip = 0
for word, value in list_of_query.items():
    if word in list_of_docs:
        for docID, values in list_of_docs[word].items():
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
    print('similarity ', getFilenameById(docID, ids), ' : ', similarity[docID])
    # if getFilenameById(docID,ids) in list_of_filenames:
    #     extract = getDocument(getFilenameById(docID,ids),sub_dir)
    # print('extracted text', extract)
