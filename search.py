import pickle
import re
import math
def search_query(query):

    normalized_idf_table = pickle.load( open( "normalized_idf.p", "rb" ) )
    map_list = pickle.load( open( "map_list.p", "rb" ) )
    filenames = pickle.load( open( "filenames.p", "rb" ) )
    url_map = pickle.load( open( "url_map.p", "rb" ) )
    filename_title =[]

    print(*filenames, sep='\n')
    row_normalized_idf_table = normalized_idf_table[1]
    total_docs = len(row_normalized_idf_table[2])

    #regular expression to find the <title> tag
    these_regex="<title>(.+?)</title>"

    #Compile the RegEx to get the pattern
    pattern=re.compile(these_regex)
    for filename in filenames:
        filename = filename[:-4]
        a = open(filename, 'r', encoding = 'utf-8',errors = 'ignore') 	
        htmltext = a.read()
        title = re.findall(pattern, htmltext)
        title = str(title).strip('[]').strip('\'')

        filename_title.append(title)

    print(*filename_title, sep='\n')

    substring_filenames = []
    for item in filenames:
        fname = item[21:]
        fname = fname[:-4]
        substring_filenames.append(fname)

    print('\n\n\n')

    # *************************** INPUTTING THE QUERY ***************************

    wordList = re.sub("[^\w]", " ", query).split() #Saving each word as an element in the list

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

    # *************************** CREATING RESULTS LIST ***************************

    results = []
    for i in range(0, len(url_map)):
        item = url_map[i]
        row = []
        row.append(item[0])
        row.append(item[1])
        get_similarity_index = substring_filenames.index(item[0]) 
        get_title_index = substring_filenames.index(item[0]) 
        get_title_index = filenames.index('Crawled_preprocessed/'+item[0]+'.txt') 
        row.append(document_similarity[get_title_index])
        row.append(filename_title[get_title_index])
        
        results.append(row)

    results = sorted(results, key = lambda x: x[2], reverse=True)#Sorting term_data in ascending order according to the word

    # *************************** FILTERING RESULTS LIST ***************************

    filtered_results = []
    for row in results:
        new_row = []
        if(row[2] !=0):
            new_row.append(row[1])
            new_row.append(row[0])
            new_row.append(row[2])
            new_row.append(row[3])
            filtered_results.append(new_row)

    with open('templates/results_upper.html', 'r') as results_html:
        upper=results_html.read()

    with open('templates/results_lower.html', 'r') as results_html:
        lower=results_html.read()

    thefile = open('templates/results.html', 'w')
    thefile.write(upper)

    result_entry = """ <div class="w3-panel w3-container w3-margin-bottom">
		            <div class="w3-container w3-white">
                                <p><b><a href='%s' target='_blank'>%s</a></b></p>
			        <p>Summary goes here</p>
		            </div>
		        </div>
                    """
    for i in range(0, len(filtered_results)):
        item = filtered_results[i]
        thefile.write(result_entry %(item[0],item[3]))
        if(i == 10):
            break
    thefile.write(lower)


