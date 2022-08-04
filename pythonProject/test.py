import os
import json
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint



url = 'https://www.taste-of-india.cz/'
odpoved = requests.get(url)
#print(odpoved.text)

soup = bs(odpoved.text,'html.parser')

sekce_menu = soup.find('ul', {'class': 'daily-menu'})

dny_menu = sekce_menu.find_all('li')
#print(dny_menu[1])

def filtruj_jidlo_ze_dne(li_tag) -> dict:
    radky = li_tag.get_text('\n').split('\n')
    radky = [r.replace('\xa0', ' ') for r in radky]
    return  {
        'den' :radky[0],
        'polevka':radky[1],
        'menu_1': radky[2],
        'menu_2': radky[3],
        'menu_3': radky[4],
        'menu_4': radky[5]
    }

def jidlo_a_cena(radek:str) -> dict:
    *jidlo,cena = radek.split(' ')
    return {' '.join(jidlo) : int(cena[:-2])}


def main():
    url = 'https://www.taste-of-india.cz/'
    odpoved = requests.get(url)
    # print(odpoved.text)

    soup = bs(odpoved.text, 'html.parser')

    sekce_menu = soup.find('ul', {'class': 'daily-menu'})
    dny_menu = sekce_menu.find_all('li')
    menu_slovnik = {}
    for den in dny_menu[1:6]:
        denni_nabidka = filtruj_jidlo_ze_dne(den)
        nazev_dne = denni_nabidka.pop('den')
        menu_slovnik[nazev_dne] = denni_nabidka
    pprint(menu_slovnik)
    uloz_menu_do_json(menu_slovnik, 'prvni_pokus.json')

def uloz_menu_do_json(menu_slovnik: dict, nazev_souboru:str):
    with open(nazev_souboru, 'w', encoding='utf8') as json_soubor:
        json.dump(menu_slovnik, json_soubor)
    print(f'Ulozeno {nazev_souboru}.json')


if __name__ == '__main__':
    main()


#oddelit jidloa cenu

#ulozit menu do json souboru


