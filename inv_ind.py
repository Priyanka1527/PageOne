#open a file
#read each word
#check if the dictionary entry exists.
#   - If it doesn't, create an entry. Insert ascending
#   - If it does, increment the term frequence in the 3rd column of the 2D array.
#f = open('Preprocessed/Acadia_National_Park.htm', 'r')

term = []
term_data = []

#Reading the file
with open('Preprocessed/Kenai_Fjords_National_Park.htm.txt','r') as f:

    #Reading the file word by word
    for line in f:
        for word in line.split():

            #For each word, checking if its term already exists in the posting list
            if(word in term):
                pos = term.index(word)
                word_data = term_data[pos]
                term_freq = word_data[2] + 1;
                word_data[2] = term_freq;
                term_data[pos] = word_data
            else:
                node = [word, 1, 1] # temp_tuple = (word, initial_doc_freq, term_freq)
                term.append(word) 
                term_data.append(node);

    #print('\n\nUnsorted Posting List:');
    #print(*term_data, sep='\n')
    posting_list = sorted(term_data, key = lambda x: x[0])
    print('\n\nSorted Posting List:');
    print(*posting_list, sep='\n')

