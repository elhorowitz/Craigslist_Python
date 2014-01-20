import urllib2, re, csv, time
from BeautifulSoup import BeautifulSoup

#Get your favs page
def getFavs(url, cookie):
    realURL = "%s" %url + "favorites?fl=%s" %cookie
    
    # Get the main page
    script = urllib2.urlopen(realURL).read()

    # Parse it with BeautifulSoup
    tree = BeautifulSoup(script)
    
    #Initialize the list of listings
    favListings = []
    
    #Find your favorite listings
    for content in tree.findAll('div', attrs={'class':'content'}):
        time.sleep(1)
        for post in content.findAll('p', attrs={'class':'row'}):
            rawDate = "%s" %post.findAll('span', attrs={'class':'date'})
            rawArea = "%s" %post.findAll('small')
            rawCat = "%s" %post.findAll('a', attrs={'class':'gc'})
            
            if not rawDate == "[]":
                date = rawDate.split('>')
                date = date[1].split('<')
                date = date[0]
                #print date
            
            if not rawArea == "[]":
                area = rawArea.split('(')
                area = area[1].split(')')
                area = area[0]
                #print area
                
            if not rawCat == "[]":
                cat = rawCat.split('data-cat="')
                cat = cat[1].split('"')
                cat = cat[0]
                #print cat
                
            rawTitle = "%s" %post.findAll('a', attrs={'href':re.compile('%s*' %cat)})[1]
            if not rawTitle == "[]":
                title = rawTitle.split('>')
                postUrl = title[0].split('"')
                postUrl = postUrl[1]
                title = title[1].split('<')
                title = title[0]
                #print postUrl, title
            
            favListings.append([date, title, area, postUrl, cat])
                
    saveListings(favListings, "FavListings")
    
def saveListings(listings, fileName):
    
    #see if listings file already exists
    try:
        with open("%s.csv" %fileName):
            #save listings to file
            for post in listings:
                newPost = True
                
                #see if this posting has already been saved
                with open("%s.csv" %fileName, "rb") as csvfileReader:
                    spamreader = csv.reader(csvfileReader, delimiter=',')
                    for row in spamreader:
                        if post[1] == row[1] and post[2] == row[2]:
                            newPost = False
                            print "duplicate: " + row[1]
                    
                #if the post is new, append it to the file
                if newPost == True:
                    with open("%s.csv" %fileName, "ab") as csvfile:
                        spamwriter = csv.writer(csvfile)
                        spamwriter.writerow([post[0], post[1], post[2], post[3], post[4]])

    except IOError:
        #set up CSV file to save the listings to
        with open("%s.csv" %fileName, "wb") as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(["Date", "Job Name", "Location", "Link to Post", "Job Category", "Notes"])
            for post in listings:
                spamwriter.writerow([post[0], post[1], post[2], post[3], post[4]])
            
    print "Listings are saved!"

#Get the craigslist specs
url = 'http://sfbay.craigslist.org/'
cookie = ''

wordInput = raw_input('\nPlease enter your favorites cookie: ')
if wordInput <> '':
    cookie = wordInput
else:
    print "Please insert your cookie!"
    
listings = getFavs(url, cookie)

