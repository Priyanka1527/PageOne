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
    input_word = input_file.read() #Word from the preprocessed files
    input_file.close()	
    token_word = word_tokenize(input_word) #tokenize using word_tokenize() in NLTK package	
    
    stop_words = set(stopwords.words("english")) #Stop words removal using Stopwords under NLTK packagae
    without_stopword = []
    without_stopword = [w for w in token_word if not w in stop_words]
 
    # stemming using Porter Stemmer in NLTK package
    stemmed_words = []
    for w in without_stopword:
        stemmed_words.append(Port_Stem.stem(w))

    output_file = codecs.open(out_dir+"/"+file_name+".txt", "w",encoding = 'utf-8',errors = 'ignore')
    output_file.write(str(stemmed_words))
    output_file.close()

for filename in os.listdir('Crawled_preprocessed/'):
    print(filename)
    text_tokenizer("Crawled_preprocessed","Crawled_tokenized",filename)
print("Tokenization Completed!!")


