"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Ondřej Vinkler
email: vinkler.prodej@gmail.com
discord: Witchho #8933
"""

import csv
import requests
from bs4 import BeautifulSoup as bs


def filtr(url):
    resp = requests.get(url)
    soup = bs(resp.text, 'html.parser')
    return soup

#odkazy na krajské města
def take_url(soup):
    hrefs = []
    for td in soup.find_all('td'):
        aa = td.find_all('a', href=True)
    # obsahuje to `href`
        if len(aa) > 0:
            a = aa[0]
            hrefs.append('https://volby.cz/pls/ps2017nss/' + a['href'])
    # neobsahuje to `href`, preskocime to
        else:
            continue
    return hrefs

seznam_obci = []
urls = take_url(filtr('https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ'))
uzemni_urovne = [url for url in urls if 'ps32?' in url]
seznam_obci.append(uzemni_urovne)

# funkce na odkazy na obce
def url_town(soup):
    take_soup = filtr(soup)
    obec_url = []
    for level in seznam_obci:
        for url in take_url(take_soup):
            if 'ps311' in url:
                obec_url.append(url)
    return obec_url

def name_town(url):
    data = filtr(url)
    for h3 in data.find("div", {"id": "publikace"}).find_all('h3'):
        if "Přebírací místo:" in h3.text:
            nazev_obce = h3.text.replace('Přebírací místo: ', '').strip()
    return nazev_obce

def code_town(url):
    kod_obce = int(url.split('&')[2].replace("xpm=", ""))
    return kod_obce

def data_town(url):
    data = filtr(url)
    list_id_sa = ['sa2','sa3','sa6']
    d_town = []
    for header in list_id_sa:
        value = data.find('td',{'headers': f'{header}'})
        value=value.text.replace('\xa0', '')
        d_town.append(int(value))
    return d_town

def political_party(data):
    data = filtr(data)
    list_party = []
    for td in data.find_all('td',{'class':'overflow_name'}):
        value = td.text.replace('\xa0','')
        list_party.append(value)
    return list_party

def political_data_1(data):
    data = filtr(data)
    list_data = []
    for td in data.find_all('td', {'headers': 't1sa2 t1sb3'}):
        value = td.text.replace('\xa0', '')
        list_data.append(value)
    return list_data

def political_data_2(data):
    data = filtr(data)
    list_data = []
    for td in data.find_all('td', {'headers': 't2sa2 t2sb3'}):
        value = td.text.replace('\xa0', '')
        list_data.append(value)
    return list_data

def political_data_c(url):
    first = political_data_1(url)
    second = political_data_2(url)
    return list(first + second)

def dat_final(url):
    odkazy = url_town(url)
    list_d = []
    for city in odkazy:
        hlasy = data_town(city)
        pol_d = political_data_c(city)
        row = [code_town(city), name_town(city), hlasy[0], hlasy[1], hlasy[2]]
        for i in pol_d:
            row.append(i)
        list_d.append(row)
    return list_d

#ukládání csv podle head_1
def main(url,name):
    data = url_town(url)[0]
    head_1 = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
    for d in political_party(data):
        head_1.append(d)
    with open(f'{name}.csv','w') as w:
        writer = csv.writer(w)
        writer.writerow(head_1)
        for row in dat_final(url):
            writer.writerow(row)
        print('Data uloženy')

if __name__ == '__main__':
    main()

data_x = 'https://www.volby.cz/pls/ps2017nss/ps31?xjazyk=CZ&xkraj=2&xnumnuts=2108'
print(main(data_x , 'data_sa'))






