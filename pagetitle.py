#Author: Priyanka Saha
#Last Updated: 5/01/2018

#NOTE: This code works on .htm files as we're extracting  metadata.

import re
import glob
from lxml import html

target_folder = 'Crawled_preprocessed/*.htm'

#regular expression to find the <title> tag
these_regex="<title>(.+?)</title>"

#Compile the RegEx to get the pattern
pattern = re.compile(these_regex)

for filename in glob.glob(target_folder):
	a = open(filename, 'r', encoding = 'utf-8',errors = 'ignore') #encoding and ignore erros to avoid charmap related issues
	htmltext = a.read() #read the htmlfiles

	#For description
	root = html.fromstring(htmltext)
	content = root.xpath('/html/head/meta[@name="description"][1]/@content')
	content = str(content).strip('[]').strip('\'')
	
	#For Title
	title = re.findall(pattern,htmltext) #apply regex extracted pattern to the html file that was read
	title = str(title).strip('[]').strip('\'') #converted list objects to string to get rid of [] and Quotes


	print("Page Title: ", title, "\n")
	print("Description: ", content)
	print("\n\n")


