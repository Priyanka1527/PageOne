import pickle
import re
import math
class search:
    normalized_idf_table = pickle.load( open( "normalized_idf.p", "rb" ) )
    filenames = pickle.load( open( "filenames.p", "rb" ) )

    row_normalized_idf_table = normalized_idf_table[1]
    total_docs = len(row_normalized_idf_table[2])

    while(True):

        print('\n\n\n')

        # *************************** INPUTTING THE QUERY ***************************

        query = input('Enter your search query:') #Accepting query from the user
            
        wordList = re.sub("[^\w]", " ",  query).split() #Saving each word as an element in the list

        # *************************** CALCULATING THE QUERY VECTOR ***************************

        #Calculating the query vector
        query_vector = []
        for node in normalized_idf_table:#length of query vector = length of the idf table
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

