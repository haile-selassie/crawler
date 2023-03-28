from bs4 import BeautifulSoup
import requests
from time import sleep as wait
import random
import re
import operator

#TODO:  Change to_visit variable to be a tree of nested tuples. So that links with tons of hrefs don't have a ton of weigh on what the next url is selected.
#       Maybe have a setting to stop at a certain amount of nests.
#       Use every homepage of a website as the root of the tree, and any subsequent branches won't have URLs of different domains.
#       Ex: github.com, education.github.com, about.linkedin.com

#TODO:  Detect if a URL points to a raw file. Count occurrance of files. Detects if URL points to a cdn or ftp server.

#TODO:  Add option to scrape information off of the websites.
#       Ex: email addresses, addresses, phone numbers, titles, or paragraphs

#TODO: Timeouts for domains

start_url = "https://www.fsf.org/twitter"
visited = list()
to_visit = list()
to_visit.append(start_url)
domains = dict()
TIME_BETWEEN_REQUESTS = 0.1

def domain_from_url(url):
    domain = re.search(r"([\d\w]{2,}\.)+[\d\w]{2,}",url).group()
    domain = domain.replace("www.","")
    return domain

def main():
    while len(to_visit) > 0:
        url = random.choice(to_visit)
        try:
            protocol = re.search(r"https*",url).group()
        except:
            print("Could not find protocol in",url)
            continue
        try:
            domain = domain_from_url(url)
        except:
            print("Could not find domain of",url)
            continue
        to_visit.remove(url)
        visited.append(url)
        webpage = None
        try:
            webpage = requests.get(url,timeout=5)
        except:
            print("Bad url or timeout",url)
            continue
        if not webpage.status_code in range(200,299):
            continue
        if domain not in domains:
            domains[domain] = 1
        else:
            domains[domain] += 1
        print(url)
        soup = BeautifulSoup(webpage.content,"html.parser")
        a_list = soup.find_all("a",href=True)
        for a in a_list:
            href = a["href"]
            if not "http" in href:
                href = f"{protocol}://{domain}{href}"
            if href not in visited and href not in to_visit and "#" not in href:
                to_visit.append(href)
        wait(TIME_BETWEEN_REQUESTS)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Crawler stopped.")
    finally:
        with open("urls.txt","a") as savefile:
            for url in visited:
                savefile.write(url.strip()+"\n")
        domains = dict(sorted(domains.items(), key=operator.itemgetter(1),reverse=True))
        print("------------------------------")
        for key in domains:
            print(domains[key],key,sep="\t")
        print("------------------------------")