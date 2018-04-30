#Author: Rohan Choudhari
#Last Updated: 4/11/2018

#NOTES:
#1. Take care of case where none of the query terms are in the search query  
#2. Take care of case where query vector is 0 because the term appears in all the docs

import glob
import os, os.path
import math
import re

#Getting the total number of docs
total_docs=0
target_folder = 'Preprocessed/*.txt'
#target_folder = 'Test_Preprocessed/*.txt'
for filename in glob.glob(target_folder):
    total_docs = total_docs+1

print('Folder Location: ', target_folder)
print('Total # of Docs: ', repr(total_docs))
print('Creating the Dictionary')

# *************************** CREATING THE DICTIONARY ***************************

term = []
term_data = []
filenames = []

#Reading the file
doc_no = 0;
#for filename in glob.glob('Test_Preprocessed/*.txt'):
for filename in glob.glob(target_folder):
    with open(filename,'r') as f:
        filenames.append(filename)

        doc_no = doc_no+1;

        #Reading the file word by word
        for line in f:
            for word in line.split():
                
                #For each word, checking if its term already exists in the posting list
                #Word exists in 'term' 
                if(word in term):
                    
                    pos = term.index(word) #getting the position of the term in the list

                    word_data = term_data[pos] #getting the element of that word from the dictionary
                    term_freq = word_data[2] + 1 # word_data[2] is term_frequency. Incrementing it
                    word_data[2] = term_freq #updating the term frequency

                    posting_list = word_data[3] # word_data[3] is the posting list. It's a list of lists
                    last_posting_item = posting_list[-1] # Pythonic way of getting the last element in the posting list

                    #Checking if we found another instance of the word in the same document
                    if(last_posting_item[0]==doc_no):#last_posting_item[0] is the doc_no
                        #Means we don't need to create a new posting item. We just increment the frequency
                        posting_freq = last_posting_item[1]
                        posting_freq = posting_freq + 1
                        last_posting_item[1] = posting_freq;
                    else:
                        #New document containing a previously recorded word so  incrementing the doc_freq
                        doc_freq = word_data[1]+1;
                        word_data[1] = doc_freq;

                        #Because this is a new document containing the word, we need a separate entry in the posting list
                        new_posting_item = []
                        new_posting_item.append(doc_no)
                        new_posting_item.append(1)
                        posting_list.append(new_posting_item)

                    word_data[2] = term_freq;
                    term_data[pos] = word_data

                # Word doesn't yet exist in 'term' 
                else:
                    posting_list = [] #This is the list for each word
                    posting_item = [] #posting_list made of one or more posting_item(s). Format: [doc_no, frequency]. See below.

                    posting_item.append(doc_no);
                    posting_item.append(1);
                    posting_list.append(posting_item) 

                    node = [word, 1, 1, posting_list] # temp_tuple = (word, initial_doc_freq, term_freq, posting_list)
                    
                    # Adding the entry for that word in term and term_data
                    term.append(word) 
                    term_data.append(node);

# *************************** CREATING THE IDF TABLE ***************************

print('Creating the IDF Table')

dict_posting_list = sorted(term_data, key = lambda x: x[0])#Sorting term_data in ascending order according to the word
#dict_posting_list = term_data
idf_table = []

for node in dict_posting_list:
    if(type(node) is list):

        #Calculating the idf
        df = node[1];
        frac = total_docs/df
        idf = math.log10(frac)

        #Appending the word and the idf
        idf_table_row = []
        idf_table_row.append(node[0])
        idf_table_row.append(idf)

        #Weight table is a list of whether the term appears in a doc. If it does,
        #that pos is 1, otherwise 0
        weight_table = []
        for x in range(1, (total_docs+1)):
            weight_table.append(0)#initializing all positions to 0

        posting_list = node[3]#getting the posting list for that word
        
        for i in range(0, len(posting_list)):
            posting_list_element = posting_list[i]
            pos = posting_list_element[0]
            tf = posting_list_element[1]
            weight_table[pos-1] = tf*idf#Marking it as 1 wherever the term occurs

        idf_table_row.append(weight_table)

        idf_table.append(idf_table_row)

# *************************** CALCULATING DOCUMENT VECTORS ***************************

print('Calculating Document Vectors')

#Declaring and initializing the document_vectors list
document_vectors = []
for i in range(0, total_docs):
    document_vectors.append(0);

for node in idf_table:
    weight_table = node[2] #Getting the weight_table for each word
    #Getting the sum of squares of each weight 
    for i in range(0, total_docs):
        weight_per_doc = weight_table[i];
        document_vectors[i] = document_vectors[i]+weight_per_doc*weight_per_doc;

#Calculating the square root of the sum of square of weights of each word
# (Psst: Getting the length of the vector)
for i in range(0, len(document_vectors)):
       vector = document_vectors[i]
       vector = math.sqrt(vector)
       document_vectors[i] = vector

# *************************** CALCULATING NORMALIZED WEIGHTS ***************************

print('Calculating Normalized Weights')

normalized_idf_table = []

#Dividing the weights by the length of the document vector to get the normalized values
for row in idf_table:
    weight_table = row[2]
    normalized_weight_table = []
    for i in range(0, len(weight_table)):
        doc_vector = document_vectors[i]
        normalized_weight = weight_table[i]/document_vectors[i]
        normalized_weight_table.append(normalized_weight)

    normalized_row = []
    normalized_row.append(row[0])
    normalized_row.append(row[1])
    normalized_row.append(normalized_weight_table)
    normalized_idf_table.append(normalized_row)

# *************************** INPUTTING THE QUERY ***************************

query = input('Enter your search query:') #Accepting query from the user
    
wordList = re.sub("[^\w]", " ",  query).split() #Saving each word as an element in the list

# *************************** CALCULATING THE QUERY VECTOR ***************************

#Calculating the query vector
query_vector = []
for node in idf_table:#length of query vector = length of the idf table
    count = 0;
    term = node[0]
    term_idf = node[1]
    query_vector_row = []
    for i in range(0, len(wordList)):
        query_term = wordList[i]
        if(term == query_term):
            count = count+1;
    query_vector_row.append(term)
    query_vector_row.append(count*term_idf)#idf
    query_vector.append(query_vector_row)

# *************************** CALCULATING THE NORMALIZED QUERY VECTOR ***************************

#Calculating the sum of sqaures
sum_of_squares = 0
for node in query_vector:
    idf = node[1]
    sum_of_squares = sum_of_squares+idf*idf 

#Getting the square root 
vector_length = math.sqrt(sum_of_squares)

#Normalizing
query_vector_normalized = []
for node in query_vector:
    row = []
    idf = node[1]
    row.append(node[0])
    row.append(idf/vector_length)
    query_vector_normalized.append(row)


# *************************** CALCULATING THE SIMILARITY ***************************
document_similarity = []
indices = []
for i in range(0, total_docs):
    document_similarity.append(0)

for i in range(0, len(normalized_idf_table)):
    row_doc = normalized_idf_table[i]
    term_idf_table = row_doc[2]

    row_query = query_vector_normalized[i]

    if(row_query[1] == 0):
        continue

    for i in range(0, total_docs):
        document_similarity[i] = document_similarity[i]+row_query[1]*term_idf_table[i]

results = []
for i in range(0, len(document_similarity)):
    row = []
    row.append(filenames[i])
    row.append(document_similarity[i])
    
    results.append(row)

results = sorted(results, key = lambda x: x[1], reverse=True)#Sorting term_data in ascending order according to the word

print(*[i for i in results if i[1] != 0], sep = '\n')

