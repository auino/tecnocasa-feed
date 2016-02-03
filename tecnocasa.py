#!/bin/python
import web
import requests
from datetime import datetime
from BeautifulSoup import BeautifulSoup

DESTINATIONPROPERTY="CIVIL"
MISSION="acquis"
TOWNID=""
PAGESIZE=10
BASEURL="http://m.tecnocasa.it/annunci/immobili/"
REFERER="http://m.tecnocasa.it/"

DOMAINBASEURL="http://www.tecnocasa.it"

# returns an offer object from html code
def getoffer(html):
	res = {}
	soup = BeautifulSoup(html)
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
	# returning result
	return res

# returns all the offers for the relative page and appends them to the offers list
def getoffers(page, lat, lon, radius, price, size):
	offers = []
	FULLURL=BASEURL+"?searchRequest.radius="+str(radius)+"&searchRequest.price="+str(price)+"&pageSize="+str(PAGESIZE)+"&searchRequest.latitude="+str(lat)+"&searchRequest.pageNumber="+str(page)+"&searchRequest.destinationProperty="+str(DESTINATIONPROPERTY)+"&searchRequest.townId="+str(TOWNID)+"&searchRequest.mobile=true&searchRequest.longitude="+str(lon)+"&searchRequest.mission="+str(MISSION)
	print FULLURL
	response = requests.get(FULLURL, headers={'Referer': REFERER})
	html = response.text

	soup = BeautifulSoup(html)
	html = soup.findAll('ul')
	html = str(html[0])

	soup = BeautifulSoup(html)
	els = soup.findAll('li')
	els = els[2:]
	for el in els:
		# getting element data
		offer = getoffer(str(el))
		if int(offer['price']) > int(price): continue
		if size == None or offer['size'] == None or int(size) > int(offer['size']): continue
		offers.append(offer)
	return offers

urls = (
	'/', 'index',
	'/feed/', 'feed'
)

render = web.template.render('templates/', cache=False)

app = web.application(urls, globals())

class index:
	def GET(self): return render.index()

class feed:
	def GET(self):
		web.header('Content-Type', 'text/xml')
		d = web.input()
		url = None
		offers = []
		for p in range(0, int(d['pages'])):
			print p
			offers += getoffers(p, d['lat'], d['lon'], d['radius'], d['price'], d['size'])
		date = datetime.today().strftime("%a, %d %b %Y %H:%M:%S +0200")
		return render.feed(offers=offers, date=date, description=d['description'])

web.webapi.internalerror = web.debugerror

if __name__ == '__main__': app.run()
