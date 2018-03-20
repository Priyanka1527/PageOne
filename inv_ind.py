#open a file
#read each word
#check if the dictionary entry exists.
#   - If it doesn't, create an entry. Insert ascending
#   - If it does, increment the term frequency in the tuple of that term.
import glob

term = []
term_data = []

#Reading the file
doc_no = 0;
for filename in glob.glob('Preprocessed/*.txt'):
    print(filename)
    with open(filename,'r') as f:

        doc_no = doc_no+1;
        print(doc_no)

        #Reading the file word by word
        for line in f:
            for word in line.split():
                
                #For each word, checking if its term already exists in the posting list
                if(word in term):
                    
                    pos = term.index(word) #getting the position of the term in the list

                    word_data = term_data[pos] #getting the element of that word from the dictionary
                    term_freq = word_data[2] + 1 # word_data[2] is term_frequence. Incrementing it

                    posting_list = word_data[3] # word_data[3] is the posting list. It's a list of lists
                    last_posting_item = posting_list[-1] # Pythonic way of getting the last element in the posting list
                    #above statement returns int if there is only 1 element in the list. returns a list if there are more than 1 elements

                    if(type(last_posting_item) is int): #If true, there is only 1 element in the list
                        if(posting_list[0]==doc_no):
                            # an element for this document does exist in the posting list. Incrementing its frequency
                            posting_freq = posting_list[1]
                            posting_freq = posting_freq + 1
                            posting_list[1] = posting_freq;
                        else:
                            # if an element for this document doesn't exist in the posting list, create one
                            new_posting_item = []
                            new_posting_item.append(doc_no)
                            new_posting_item.append(1)
                            posting_list.append(new_posting_item)
                    else:
                        # posting list has more than 1 element.
                        if(last_posting_item[0]==doc_no):
                            posting_freq = last_posting_item[0]
                            posting_freq = posting_freq + 1
                            last_posting_item[1] = posting_freq;
                        else:
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
posting_list = sorted(term_data, key = lambda x: x[0])
print('\n\nSorted Posting List:');
print(*posting_list, sep='\n')

