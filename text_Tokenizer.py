#Author: Priyanka Saha
#Last Updated: 4/29/2018

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
import codecs

Port_Stem = PorterStemmer()

def text_tokenizer(in_dir, out_dir, file_name):
    input_file = codecs.open(in_dir+"/"+file_name,'r',encoding = 'utf-8',errors = 'ignore')
    input_word = input_file.read()
    input_file.close()	
    token_word = word_tokenize(input_word) #tokenize using word_tokenize() in NLTK package
    #print(tokenized_word)	
    # remove stop words using "English" disctionary
    stop_words = set(stopwords.words("english"))
    without_stopword = []
    without_stopword = [w for w in token_word if not w in stop_words]
    #print(removedstop_word)
    # stemming using Lancaster Stemmer in NLTK package
    stemmed_words = []
    for w in without_stopword:
        stemmed_words.append(Port_Stem.stem(w))

    #print(stemmed_words)
    output_file = codecs.open(out_dir+"/"+file_name+".txt", "w",encoding = 'utf-8',errors = 'ignore')
    output_file.write(str(stemmed_words))
    output_file.close()

for filename in os.listdir('Preprocessed_test/'):
    print(filename)
    text_tokenizer("Preprocessed_test","Tokenized_test",filename)
print("Tokenization completed!!")

#pip3 install nltk; nltk.download('all') 
