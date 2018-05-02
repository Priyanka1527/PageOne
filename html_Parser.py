#Author: Priyanka Saha
#Last Updated: 5/01/2018


from lxml import html
from lxml.html.clean import Cleaner
import string
import os


def html_preprocessing(in_dir):
    for filename in os.listdir(in_dir):
        print(filename)
        parsing_html(in_dir,"Crawled_preprocessed",filename)
        
def ch_alpha(ch):
    if ch.isalpha():
        return ch
    else:
        return ' '

def parsing_html(in_dir,preprocessed,file_name):
    input_file = open(in_dir+"/"+file_name,"rb")
    input_str = input_file.read()
    out_file = open(preprocessed+"/"+file_name, "wb")
    out_file.write(input_str)
    
    parsed = html.parse(preprocessed+"/"+file_name)
    clean = Cleaner()
    cleaner = Cleaner.clean_html(clean, parsed)
    plaintext = cleaner.getroot().text_content() # removes markup from root and child nodes
    plaintext = plaintext.replace('\n',' ')
    plaintext = plaintext.replace('  ', ' ')
    plaintext = plaintext.replace('\t',' ')
    plaintext = ''.join(ch_alpha(ch) for ch in plaintext)
    plaintext = ' '.join(plaintext.split())
    plaintext = plaintext.lower()
    plaintext_file = open(preprocessed+"/"+file_name+".txt", "wb")
    plaintext_file.write(plaintext.encode('utf-8')) 
    plaintext_file.close()
    input_file.close()
    out_file.close()

html_preprocessing('Crawled_Pages/') 
