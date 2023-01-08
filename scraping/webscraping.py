import requests
from bs4 import BeautifulSoup
import pandas

url = 'http://example.webscraping.com'

response = requests.get(url)

if response.ok:
    links = []
    soup = BeautifulSoup(response.text, 'lxml')
    tds = soup.findAll('td')
#    print(len(tds))
#    for td in tds:
#else:
#    print(response.text)

    for td in tds:
        a = td.find('a')
        link = a['href']
        links.append('http://example.webscraping.com' + link)

    print(links)