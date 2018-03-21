#open a file
#read each word
#check if the dictionary entry exists.
#   - If it doesn't, create an entry. Insert ascending
#   - If it does, increment the term frequency in the tuple of that term.

import glob
import os, os.path
import math

total_docs=0
for filename in glob.glob('Preprocessed/*.txt'):
    total_docs = total_docs+1

term = []
term_data = []

#Reading the file
doc_no = 0;
#for filename in glob.glob('Test_Preprocessed/*.txt'):
for filename in glob.glob('Preprocessed/*.txt'):
    with open(filename,'r') as f:

        doc_no = doc_no+1;

        #Reading the file word by word
        for line in f:
            for word in line.split():
                
                #For each word, checking if its term already exists in the posting list
                if(word in term):
                    
                    pos = term.index(word) #getting the position of the term in the list

                    word_data = term_data[pos] #getting the element of that word from the dictionary
                    term_freq = word_data[2] + 1 # word_data[2] is term_frequence. Incrementing it
                    word_data[2] = term_freq #updating the term frequency

                    posting_list = word_data[3] # word_data[3] is the posting list. It's a list of lists
                    last_posting_item = posting_list[-1] # Pythonic way of getting the last element in the posting list

                    if(last_posting_item[0]==doc_no):
                        posting_freq = last_posting_item[1]
                        posting_freq = posting_freq + 1
                        last_posting_item[1] = posting_freq;
                    else:
                        doc_freq = word_data[1]+1;
                        word_data[1] = doc_freq;

                        new_posting_item = []
                        new_posting_item.append(doc_no)
                        new_posting_item.append(1)
                        posting_list.append(new_posting_item)

                    word_data[2] = term_freq;
                    term_data[pos] = word_data
                else:
                    posting_list = []
                    posting_item = []
                    posting_item.append(doc_no);
                    posting_item.append(1);
                    posting_list.append(posting_item)

                    node = [word, 1, 1, posting_list] # temp_tuple = (word, initial_doc_freq, term_freq, posting_list)

                    term.append(word) 
                    term_data.append(node);

        #print('\n\nUnsorted Posting List:');
        #print(*term_data, sep='\n')
dict_posting_list = sorted(term_data, key = lambda x: x[0])
#print(*dict_posting_list, sep='\n')


idf_table = []

for node in dict_posting_list:
    if(type(node) is list):

        df = node[1];
        frac = total_docs/df
        idf = math.log10(frac)

        idf_table_row = []
        idf_table_row.append(node[0])
        idf_table_row.append(idf)

        weight_table = []
        for x in range(1, (total_docs+1)):
            weight_table.append(0)

        posting_list = node[3]
        
        #print(node[0])
        for i in range(0, len(posting_list)):
            posting_list_element = posting_list[i]
            #print(posting_list_element)
            pos = posting_list_element[0]
            #print(pos)
            weight_table[pos-1] = 1

        idf_table_row.append(weight_table)

        idf_table.append(idf_table_row)


#print(*idf_table, sep='\n')
for i in range(1, len(idf_table)):
    print(dict_posting_list[i])
    print(idf_table[i])
    print('')

    
    
