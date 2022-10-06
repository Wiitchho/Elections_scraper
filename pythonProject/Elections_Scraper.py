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


def take_url(soup):
    '''
    Vezme argument odkazu a vytáhne veškeré odkazy obsahující href
    pokud neobsahuje href, přeskočí to a pokračuje dál.
    '''
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


def deep():
    '''Vytáhne odkazy na všechny obce '''
    seznam_obci = []
    urls = take_url(filtr('https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ'))
    uzemni_urovne = [url for url in urls if 'ps32?' in url]
    seznam_obci.append(uzemni_urovne)


def url_town(soup):
    '''Vezme odkaz na hlubší procházení'''
    take_soup = filtr(soup)
    obec_url = []
    for level in deep():
        for url in take_url(take_soup):
            if 'ps311' in url:
                obec_url.append(url)
    return obec_url


def name_town(url):
    '''Funkce projede přes filtr a najde jméno obcí.
     Vrátí je v seznamu'''
    data = filtr(url)
    t = []
    for h3 in data.find("div", {"id": "publikace"}).find_all('h3'):
        if "Obec:" in h3.text:
            value = h3.text.replace('Obec: ', '').strip()
            t.append(value)
    return t


def code_town(url):
    '''
    Funkce rozkrájí odkaz pomoci metody split
     a v pořadí &[2] najde xobec= kód
    '''
    kod_obce = int(url.split('&')[2].replace("xobec=", ""))
    return kod_obce


def data_town(url):
    '''vybere data, které budeme ukládat pod hlavičkou do csv souboru'''
    data = filtr(url)
    list_id_sa = ['sa2', 'sa3', 'sa6']
    d_town = []
    for header in list_id_sa:
        value = data.find('td', {'headers': f'{header}'})
        value = value.text.replace('\xa0', '')
        d_town.append(int(value))
    return d_town


def political_data_c(data):
    '''Funkce na tahání politických stran a počet voličů.
    return: list politických stran. '''
    data = filtr(data)
    list_data = []
    for td in data.find_all('td', {'headers': 't1sa2 t1sb3'}):
        value = td.text.replace('\xa0', '')
        list_data.append(value)
    for td in data.find_all('td', {'headers': 't2sa2 t2sb3'}):
        value = td.text.replace('\xa0', '')
        list_data.append(value)
    return list_data


def name_region(url):
    '''funkce prpo ukládání názvu souboru podle územního celku'''
    data = filtr(url)
    s = []
    for div in data.find('div', {'id': 'publikace'}).find_all('h3'):
        value = div.text.replace('\n', '')
        s.append(value)
    return s[1]


def dat_final(url):
    '''Seřazení dat k sobě. Return: data které následně budeme ukládat.'''
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


def csv_save(url, name):
    '''Ukládání do csv souboru, hlavička head_1 + politické strany'''
    data = url_town(url)[0]
    head_1 = [
        'Kód obce',
        'Název obce',
        'Voliči v seznamu',
        'Vydané obálky',
        'Platné hlasy']
    for d in political_party(data):
        head_1.append(d)
    with open(f'{name}.csv', 'w') as w:
        writer = csv.writer(w)
        writer.writerow(head_1)
        for row in dat_final(url):
            writer.writerow(row)
        print('Data uloženy')


def main():
    '''Parsování Kraj vysočina, Havlíčkův Brod.'''
    url = 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6101'
    csv_save(url, name_region(url))


if __name__ == '__main__':
    main()