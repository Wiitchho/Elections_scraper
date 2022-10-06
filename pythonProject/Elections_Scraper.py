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

''' 
vezme argument odkazu a vytáhne veškeré odkazy obsahující href
pokud neobsahuje href, přeskočí to a pokračuje dál.
'''
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
'''Vezme odkaz a vytáhne z toho odkazy na hlubší procházení'''
def url_town(soup):
    take_soup = filtr(soup)
    obec_url = []
    for level in seznam_obci:
        for url in take_url(take_soup):
            if 'ps311' in url:
                obec_url.append(url)
    return obec_url

'''Funkce projede přes filtr a najde jméno obcí. 
 Vrátí je v seznamu'''
def name_town(url):
    data = filtr(url)
    t = []
    for h3 in data.find("div", {"id": "publikace"}).find_all('h3'):
        if "Obec:" in h3.text:
            value = h3.text.replace('Obec: ', '').strip()
            t.append(value)
    return t

'''Funkce rozkrájí odkaz pomoci metody split
 a v pořadí &[2] najde xobec= kód
'''
def code_town(url):
    kod_obce = int(url.split('&')[2].replace("xobec=", ""))
    return kod_obce

'''vybere data, které budeme ukládat pod hlavičkou do csv souboru'''
def data_town(url):
    data = filtr(url)
    list_id_sa = ['sa2','sa3','sa6']
    d_town = []
    for header in list_id_sa:
        value = data.find('td',{'headers': f'{header}'})
        value=value.text.replace('\xa0', '')
        d_town.append(int(value))
    return d_town

'''Funkce na tahání politických stran a počet voličů.
První sloupec. '''
def political_data_1(data):
    data = filtr(data)
    list_data = []
    for td in data.find_all('td', {'headers': 't1sa2 t1sb3'}):
        value = td.text.replace('\xa0', '')
        list_data.append(value)
    return list_data

'''Pokračování dalšího sloupce. '''
def political_data_2(data):
    data = filtr(data)
    list_data = []
    for td in data.find_all('td', {'headers': 't2sa2 t2sb3'}):
        value = td.text.replace('\xa0', '')
        list_data.append(value)
    return list_data

'''Spojení dat pro lepší ukládání'''
def political_data_c(url):
    first = political_data_1(url)
    second = political_data_2(url)
    return list(first + second)

'''funkce prpo ukládání názvu souboru podle územního celku'''
def name_region(url):
    data = filtr(url)
    s = []
    for div in data.find('div',{'id':'publikace'}).find_all('h3'):
        value = div.text.replace('\n','')
        s.append(value)
    return s[1]

'''Seřazení dat k sobě. Return: data které následně budeme ukládat.'''
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
'''Ukládání do csv souboru, hlavička head_1 + politické strany'''
def csv_save(url,name):
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

'''Parsování Kraj vysočina, Havlíčkův Brod.'''
def main():
    url = 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6101'
    csv_save(url,name_region(url))

if __name__ == '__main__':
    main()







