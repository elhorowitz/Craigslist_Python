import urllib2, re, csv
from BeautifulSoup import BeautifulSoup


#Get the listings
def getListings(url, category, subcategory, keywords):
    
    realURL = "%s" %url + "%s" %category
    subURL = "%s" %url + "%s" %subcategory
    
    for keyword in keywords:
        words = keyword.replace(" ","+")
        searchURL = "%s" %url + "search/%s" %category + "?zoomToPosting=&catAbb=%s" %category + "&query=%s" %words + "&excats="
        
        # Get the page
        script = urllib2.urlopen(searchURL).read()
    
        # Parse it with BeautifulSoup
        tree = BeautifulSoup(script)
    
        for content in tree.findAll('div', attrs={'class':'content'}):
            for post in content.findAll('p', attrs={'class':'row'}):
                date = post.findAll('span', attrs={'class':'date'})
                area = post.findAll('small')
                cat = post.findAll('a', attrs={'class':'gc'})
                title = post.findAll('a', attrs={'href':'/sfc/%s*' %cat})
                print title, date, area, cat
                






#Get the craigslist specs
url = 'http://sfbay.craigslist.org/'
category = 'jjj'
subcategory = 'jjj0'
keywords = []

wordInput = raw_input('\nPlease enter keywords to search on, separated by commas: ')
if wordInput <> '':
    keywords = wordInput.split(',')
    
listings = getListings(url, category, subcategory, keywords)

