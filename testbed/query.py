# Simple extended boolean search engine: query module
# Hussein Suleman
# 14 April 2016

import re
import math
import sys
import os

import porter

import parameters

import relevanceScoring
from collections import Counter



# Main search Function
def getResults(*args):
    if len(sys.argv)<3:
       print ("Syntax: query.py <collection> <query>")
       exit(0)

    # construct collection and query
    collection = sys.argv[1]
    query = ''
    arg_index = 2
    while arg_index < len(sys.argv):
       query += sys.argv[arg_index] + ' '
       arg_index += 1

    # clean query
    if parameters.case_folding:
       query = query.lower ()
    query = re.sub (r'[^ a-zA-Z0-9]', ' ', query)
    query = re.sub (r'\s+', ' ', query)
    query_words = query.split (' ')

    # create accumulators and other data structures
    accum = {}
    filenames = []
    p = porter.PorterStemmer ()

    # get N
    f = open (collection+"_index_N", "r")
    N = eval (f.read ())
    f.close ()

    # get document lengths/titles
    titles = {}
    f = open (collection+"_index_len", "r")
    lengths = f.readlines ()
    f.close ()

    # get index for each term and calculate similarities using accumulators
    for term in query_words:
        if term != '':
            if parameters.stemming:
                term = p.stem (term, 0, len(term)-1)
            if not os.path.isfile (collection+"_index/"+term): # remember we have an inverted file/term
               continue                                         # done during indexing
            f = open (collection+"_index/"+term, "r")
            lines = f.readlines ()
            idf = 1
            if parameters.use_idf:
               df = len(lines)
               idf = 1/df
               if parameters.log_idf:
                  idf = math.log (1 + N/df)
            for line in lines:
                mo = re.match (r'([0-9]+)\:([0-9\.]+)', line)
                if mo:
                    file_id = mo.group(1)
                    tf = float (mo.group(2))
                    if not file_id in accum:
                        accum[file_id] = 0
                    if parameters.log_tf:
                        tf = (1 + math.log (tf))
                    accum[file_id] += (tf * idf)  #adding the similarity score to the accumulator
            f.close()

    # parse lengths data and divide by |N| and get titles
    for l in lengths:
       mo = re.match (r'([0-9]+)\:([0-9\.]+)\:(.+)', l)
       if mo:
          document_id = mo.group (1)
          length = eval (mo.group (2))
          title = mo.group (3)
          if document_id in accum:
             if parameters.normalization:
                accum[document_id] = accum[document_id] / length
             titles[document_id] = title

    # print top ten results
    result = sorted (accum, key=accum.__getitem__, reverse=True)
    for i in range (min (len (result), 10)):
       print ("{0:10.8f} {1:5} {2}".format (accum[result[i]], result[i], titles[result[i]]))

    return result

results = getResults()
# get Documents

allDocs = relevanceScoring.getDocs("testbed/Doc_Collection")
# print("Doc 15:", allDocs[20])



# extension for blind relevance feedback
def relFeedback(results, numTerms):

        print("Blind Feedback")
        query2 = getPopularTerms(results, numTerms)
        print(query2)
        sys.argv[2] = query2
        getResults()


# read the top ten relevant documents into an array
def getPopularTerms(results, k_terms):

    relDocs = []

    for docId in results:
        relDocs.append(allDocs[int(docId)])


    # Tokenize document into terms
    words = []
    for doc in relDocs:
        # Use regular expression to split the document into terms and ignore punctuation
        words.extend(re.findall(r'\b\w+\b', doc.lower()))

    # Count the occurrences of each word
    word_counter = Counter(words)

    # Find the most popular words
    most_common_words = word_counter.most_common(k_terms)

    # Concatenate the most popular words into a single string
    concatenated_string = " ".join([word for word, count in most_common_words])

    # Display the concatenated string
    print("The concatenated string of most popular words is:")
    print(concatenated_string)

    with open("testbed/popularTerms.txt", "a") as file:
        file.write("Query\n" + sys.argv[2] + "\n")
        file.write("Popular_Terms\n" + concatenated_string + "\n")

    return concatenated_string


# Second Search with blind relevance feedback

relFeedback(results, 10)