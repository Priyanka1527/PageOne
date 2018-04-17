import requests
from bs4 import BeautifulSoup

#web spider to crawl the pages from IMDB
def movie_spider():
	url = 'https://www.imdb.com/chart/moviemeter?ref_=nv_mv_mpm_8' #URL to start the crawl from
	source_code = requests.get(url)#requeting and storing the source code of the page
	plain_text = source_code.text #get the plain text from the webpage
	soup = BeautifulSoup(plain_text, "lxml") #creating a beautifulsoupobject and specifying to be parsed by lxml parser
	for link in soup.findAll('td', {'class': 'titleColumn'}): #the <td> class for links were found to be titlecolumn on inspection
		href = "https://www.imdb.com" + link.find('a').get('href') #concatenating the retrived title URL with the domain of IMDB
		title = link.find('a').string #to retrive the title from the <a> tag
		#print(href)
		#print(title)
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
				href = "https://www.imdb.com" + link.get('href')
			print(href)


movie_spider()


