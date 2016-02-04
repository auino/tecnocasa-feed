#!/bin/python

# 
# tecnocasa-feed
# Author: Enrico Cambiaso
# Email: enrico.cambiaso[at]gmail.com
# GitHub project URL: https://github.com/auino/tecnocasa-feed
# 

import web
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# --- --- --- --- ---
# CONFIGURATION BEGIN
# --- --- --- --- ---

# Basic server configuration

# listening address used by the server (i.e. set it to "127.0.0.1" to only accept connections from localhost)
LISTENADDRESS="0.0.0.0"
# listening port of the server
LISTENPORT=8080
# how many pages to surf looking for results
PAGESCOUNT=3

# Tecnocasa official parameters
# If needed, you can tune these parameters accordingly to your needs, starting from http://m.tecnocasa.it

DESTINATIONPROPERTY="CIVIL"
MISSION="acquis"
TOWNID=""
PAGESIZE=10
BASEURL="http://m.tecnocasa.it/annunci/immobili/"
REFERER="http://m.tecnocasa.it/"
DOMAINBASEURL="http://www.tecnocasa.it"

# --- --- --- --- ---
#  CONFIGURATION END 
# --- --- --- --- ---

# this method returns an offer object from html code
def getoffer(html):
	res = {}
	# parsing the html string
	soup = BeautifulSoup(html, 'html.parser')
	# url
	res['url'] = DOMAINBASEURL+str(soup.find('a')['href'])
	if '?' in res['url']: res['url'] = res['url'][:res['url'].index('?')]
	# id
	res['id'] = res['url']
	# image
	res['image'] = DOMAINBASEURL+str(soup.find('img')['src'])
	# location
	res['location'] = soup.findAll('strong')[1].contents[0].replace('\n', '').strip()
	# location (big city level)
	res['location_left'] = res['location']
	try: res['location_left'] = res['location_left'][:res['location_left'].index(' - ')]
	except: pass
	# location (small city level)
	res['location_right'] = res['location']
	try: res['location_right'] = res['location_right'][res['location_right'].index(' - ')+3:]
	except: pass
	# description
	res['description'] = soup.findAll('p')[2].contents[0].replace('\n', '').strip()
	# rooms
	res['rooms'] = None
	try: res['rooms'] = res['description'][:res['description'].index(' ')]
	except: pass
	# size
	res['size'] = None
	try:
		tmp = res['description'][res['description'].index('-')+2:]
		tmp = tmp[tmp.index(' ')+1:]
		res['size'] = tmp[:tmp.index(' ')]
	except: pass
	# price
	res['price'] = None
	try:
		tmp = soup.findAll('strong')[2].contents[0].replace('\n', '').strip()
		res['price'] = tmp[tmp.index(' ')+1:].replace('.', '')
	except: pass
	# returning the offer object result
	return res

# returns all the offers for the relative page and appends them to the offers list
def getoffers(page, lat, lon, radius, price, size):
	offers = []
	# building complete url of real estate service
	FULLURL=BASEURL+"?searchRequest.radius="+str(radius)+"&searchRequest.price="+str(price)+"&pageSize="+str(PAGESIZE)+"&searchRequest.latitude="+str(lat)+"&searchRequest.pageNumber="+str(page)+"&searchRequest.destinationProperty="+str(DESTINATIONPROPERTY)+"&searchRequest.townId="+str(TOWNID)+"&searchRequest.mobile=true&searchRequest.longitude="+str(lon)+"&searchRequest.mission="+str(MISSION)
	# making the http request
	response = requests.get(FULLURL, headers={'Referer': REFERER})
	html = response.text

	# filtering the result, retrieving the list of offers
	soup = BeautifulSoup(html, 'html.parser')
	html = soup.findAll('ul')
	html = str(html[0])
	soup = BeautifulSoup(html, 'html.parser')
	els = soup.findAll('li')
	els = els[2:]
	for el in els:
		# getting element data
		offer = getoffer(str(el))
		# checking if offer price is higher than the maximum price specified by the user (it may be, e.g., for sponsored offers)
		if int(offer['price']) > int(price): continue
		# checking if offer size is lower than the minimum size specified by the user (real estate service does not offers the way to filter on such parameter, on mobile website)
		if offer['size'] == None or int(size) > int(offer['size']): continue
		# appending the current offer to the results list
		offers.append(offer)
	# returing the result
	return offers

# list of urls accepted by the web server and relative callbacks/triggers
urls = (
	'/', 'index',
	'/feed/', 'feed'
)

# index trigger class
class index:
	def GET(self): return render.index()

# feed trigger class
class feed:
	def GET(self):
		# changing returned content type
		web.header('Content-Type', 'text/xml')
		# reading input parameters
		d = web.input()
		offers = []
		# surfing different pages of results and appending the found offers to the output
		for p in range(0, PAGESCOUNT): offers += getoffers(p, d['lat'].replace('.', ','), d['lon'].replace('.', ','), d['radius'], d['price'], d['size'])
		# getting current date
		date = datetime.today().strftime("%a, %d %b %Y %H:%M:%S +0200")
		# returning the resulting page
		return render.feed(offers=offers, date=date, description=d['description'])

# Web Service application class
class WebServiceApplication(web.application):
	def run(self, *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, (LISTENADDRESS, LISTENPORT))

render = web.template.render('templates/', cache=False)

app = WebServiceApplication(urls, globals())

web.webapi.internalerror = web.debugerror

if __name__ == '__main__': app.run()
