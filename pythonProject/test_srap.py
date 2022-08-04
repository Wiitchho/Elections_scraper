from pprint import pprint
import csv
import os
import requests
from bs4 import BeautifulSoup as bs



def filtr(url):
    resp = requests.get(url)
    soup = bs(resp.text, 'html.parser')
    return soup

def take_url(soup):
    hrefs = []
    for td in soup.find_all('td'):
        aa = td.find_all('a', href=True)
    # obsahuje to `href`
        if len(aa) > 0:
            a = aa[0]
            hrefs.append(a['href'])
    # neobsahuje to `href`, preskocime to
        else:
            continue
    return hrefs

def scrap_next(url):
    seznam_o = []
    odkaz = requests.get(url)
    text = bs(odkaz.text,'html.parser')
    for tr in text.find_all('tr'):
        aa = tr.find_all('a', href=True)
        if len(aa) >0:
            a = aa[0]
            seznam_o.append('https://volby.cz/pls/ps2017nss/' + a['href'])
    return seznam_o


pprint(scrap_next('https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8106'))



def add_all_url(hrefs):
    all_hrefs = []
    for href in hrefs:
        all_hrefs.append('https://volby.cz/pls/ps2017nss/' + href)
    return all_hrefs

#pprint(add_all_url(take_url(filtr("https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"))))

def second_pars(url2):
    hotovo = filtr(url2)
    for tag in hotovo.find_all("td"):
        print(tag)

#second_pars('https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8106')

def browser(odkaz):
    hledam_cesty = odkaz.find_all('td',{'class':'cislo'})
    sezna_m =[]
    for d_ata in hledam_cesty:
        sezna_m.append(d_ata)
    pprint(sezna_m)



