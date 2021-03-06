#Author: Priyanka Saha
#Last updated on: May 01, 2018

import requests
import io
from bs4 import BeautifulSoup
from timeit import default_timer as timer
import pickle

#web spider to crawl the pages from IMDB
url_crawled =[]
def trading_spider():

	#Seed URLs to start the crawl in multiple thread
	url = 'https://www.investopedia.com/terms/m/marketrisk.asp' 
	url_seed2 = 'https://www.investopedia.com/active-trading/' 
	url_seed3 = 'https://www.investopedia.com/bitcoin/'
	url_seed4 = 'https://www.investopedia.com/news/'
	url_seed5 = 'https://www.investopedia.com/tech/'

	#requeting and storing the source code of the page
	source_code = requests.get(url)
	source_code2 = requests.get(url_seed2)
	source_code3 = requests.get(url_seed3)
	source_code4 = requests.get(url_seed4)
	source_code5 = requests.get(url_seed5)

	#get the plain text from the webpage
	plain_text = source_code.text 
	plain_text2 = source_code2.text
	plain_text3 = source_code3.text
	plain_text4 = source_code4.text
	plain_text5 = source_code5.text

	#creating a beautifulsoupobject and specifying to be parsed by lxml parser
	soup = BeautifulSoup(plain_text, "lxml") 
	soup2 = BeautifulSoup(plain_text2, "lxml")
	soup3 = BeautifulSoup(plain_text3, "lxml")
	soup4 = BeautifulSoup(plain_text4, "lxml")
	soup5 = BeautifulSoup(plain_text5, "lxml")


	for link in soup.findAll('p'): #inspecting the <p> tag for links
		if link.find('a') is not None:
			href = "https://www.investopedia.com" + link.find('a').get('href')
			get_single_item_data(href) #gather links from each page

	for link in soup2.findAll('h3', {'class': 'item-title'}): #the <h3> class for links were found to be "item-title" on inspection
		if link.find('a') is not None:
			href = "https://www.investopedia.com" + link.find('a').get('href')
			get_single_item_data(href) #gather links from each page

	for link in soup3.findAll('ul', {'class': 'cl cl-5'}): #the <ul> class for links were found to be "cl cl-5" on inspection
		if link.find('a') is not None:
			href = "https://www.investopedia.com" + link.find('a').get('href')
			get_single_item_data(href) #gather links from each page

	for link in soup4.findAll('h3', {'class': 'item-title'}): #the <h3> class for links were found to be "item-title" on inspection
		if link.find('a') is not None:
			href = "https://www.investopedia.com" + link.find('a').get('href')
			get_single_item_data(href) #gather links from each page

	for link in soup5.findAll('h3', {'class': 'item-title'}): #the <h3> class for links were found to be "item-title" on inspection
		if link.find('a') is not None:
			href = "https://www.investopedia.com" + link.find('a').get('href')
			get_single_item_data(href) #gather links from each page
		

def get_single_item_data(item_url):
	source_code = requests.get(item_url)
	plain_text = source_code.text #get the plain text from the webpage
	soup = BeautifulSoup(plain_text, "lxml") #creating a beautifulsoupobject
	for link in soup.findAll('a'):
		if link.get('href') is not None:
			if link.get('href').startswith('http'):
				href = link.get('href')
			else:
				href = "https://www.investopedia.com" + link.get('href')
			#print(href)
			if href not in url_crawled: #check for duplicates
				if (href.find('facebook') is -1 and href.find('linkedin') is -1 and href.find('twitter') is -1): #URL filtering for social media sites
					if(href.find('investopedia') is not -1):
						url_crawled.append(href)
						print(href)


#start = timer()
trading_spider()
#print(url_crawled)
size = len(url_crawled)
print("The number of URLs crawled: ",size)
url_list = open('url_list.txt', 'w')
filename_url_list = []

#download the webpages in html format from the crawled URLs
for i in range(0,size):
	filename = 'file_' + str(i) + '.htm'
	row =[]
	row.append(filename)
	row.append(url_crawled[i])
	filename_url_list.append(row)
	print(filename)
	with io.open(filename, 'wb') as f:
		r = requests.get(url_crawled[i], allow_redirects=True)
		url_list.write(url_crawled[i] + '\n')
		f.write(r.content)
print(*filename_url_list, sep='\n')
url_list.close()
pickle.dump(filename_url_list, open('url_map.p', 'wb'))
#end = timer()
#print("Time taken to crawl these documents is :", end - start)



