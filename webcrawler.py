### Adding a comment to update per the instructions in the Question 2 of the assignment

from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request

### Question 1 ###

seed_url = "https://www8.gsb.columbia.edu"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them

maxNumUrl = 50; #set the maximum number of urls to visit
print("Starting with url="+str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  #creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        print("seed_url=" + seed_url)
        print("original childurl=" + o_childurl)
        print("childurl=" + childUrl)
        print("seed_url in childUrl=" + str(seed_url in childUrl))
        print("Have we seen this childUrl=" + str(childUrl in seen))
        if seed_url in childUrl and childUrl not in seen:
            print("***urls.append and seen.append***")
            urls.append(childUrl)
            seen.append(childUrl)
        else:
            print("######")

print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))
print("List of seen URLs:")
for seen_url in seen:
    print(seen_url)

### Question 2 ###

seed_url = "https://www.europarl.europa.eu/news/en/press-room"

urls = [seed_url]
seen = [seed_url]
opened = []
press_releases = []

maxNumUrl = 200  # Increase the maximum as 50 might not be enough to find 10 press releases with "crisis".

while len(urls) > 0 and len(press_releases) < 10 and len(opened) < maxNumUrl:
    try:
        curr_url = urls.pop(0)
        req = urllib.request.Request(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= " + curr_url)
        continue

    soup = BeautifulSoup(webpage, 'html.parser')

    # Check if it's a press release related to plenary sessions
    plenary_tag = soup.find('span', {'class': 'ep_name'}, string='Plenary session')
    if plenary_tag:
        content = soup.get_text()
        if "crisis" in content.lower():  # check if content contains the word 'crisis'
            press_releases.append(curr_url)
            save_text_to_file(content, len(press_releases))
            continue  # Skip adding child urls if this is a press release

    for tag in soup.find_all('a', href=True):
        childUrl = tag['href']
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        if childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)

print("Number of press releases about plenary sessions containing 'crisis':", len(press_releases))
print("Press releases URLs:")
for pr_url in press_releases:
    print(pr_url)