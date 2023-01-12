import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request
url='https://www.amazon.com/b?node=16225016011&pf_rd_r=8YTV1WEXADBMR34Q87RX&pf_rd_p=e5b0c85f-569c-4c90-a58f-0c0a260e45a0'
page=urllib.request.urlopen(url,timeout=5)
soup=bs(page)
soup
prod= soup.find_all('h2', {'class': 'a-size-mini a-color-base apb-line-clamp-3 a-text-normal'})
prod
produits=[]
for e in prod :
    e=e.text
    e=e.replace('\n','')
produits.append(e)
produits
pri_tot= soup.find_all('span', {'class': 'a-price-whole'})
pri_tot
prix_initials = []
for e in pri_tot :
    e = e.text
prix_initials.append (e)
prix_initials
prix_initials = []
cons= soup.find_all('span', {'class': 'a-size-base a-color-secondary a-text-normal'})
cons
for e in pri_tot : \
    e = e.text
prix_initials.append (e)
prix_initials