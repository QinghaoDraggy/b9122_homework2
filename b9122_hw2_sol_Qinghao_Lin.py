from bs4 import BeautifulSoup
import urllib.request

def save_text_to_file(part, content, index):
    filename = f"{part}_{index}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Saved content to {filename}")


### Question 1 ###

seed_url = "https://press.un.org/en"

urls = [seed_url]
seen = [seed_url]
opened = []
press_releases = []

maxNumUrl = 1000  # increased the maximum number as 50 might not be enough to find 10 press releases with "crisis"

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

    # Check if it's a press release
    press_release_tag = soup.find('a', {'href': '/en/press-release', 'hreflang': 'en'})
    if press_release_tag:
        content = soup.get_text()
        if "crisis" in content.lower():  # check if content contains the word 'crisis'
            press_releases.append(curr_url)
            save_text_to_file(1, content, len(press_releases))
            print("Found a press release with 'crisis' in it: " + curr_url)
            continue  # Skip adding child urls if this is a press release

    for tag in soup.find_all('a', href=True):
        childUrl = tag['href']
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        if childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)

print("Number of press releases containing 'crisis':", len(press_releases))
print("Press releases URLs:")
for pr_url in press_releases:
    print(pr_url)


### Question 2 ###

seed_url = "https://www.europarl.europa.eu/news/en/press-room"

urls = [seed_url]
seen = [seed_url]
opened = []
press_releases = []

maxNumUrl = 1000  # Increase the maximum as 50 might not be enough to find 10 press releases with "crisis".

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
            save_text_to_file(2, content, len(press_releases))
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
