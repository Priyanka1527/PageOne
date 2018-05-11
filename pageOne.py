#from inv_ind.py import inverted_index

import search
class main:
    #vector_space = inverted_index()  

    # *************************** INPUTTING THE QUERY ***************************

    k = input('Enter value of k:') #Accepting query from the user
    query = input('Enter your search query:') #Accepting query from the user
    search.search_query(query, k)

