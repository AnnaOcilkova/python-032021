import requests
import pandas
import numpy

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/lexikon-zvirat.csv")
open("lexikon-zvirat.csv", "wb").write(r.content)

zvirata = pandas.read_csv("lexikon-zvirat.csv", sep = ';')
# pandas.set_option('display.max_columns', None)
# pandas.set_option('display.max_rows', None)

# Poslední sloupec a poslední řádek obsahují nulové hodnoty. Zbav se tohoto sloupce a řádku.

zvirata = zvirata.dropna(axis=0, how='all')
zvirata = zvirata.dropna(axis=1, how='all')

# Nastav sloupec id jako index pomocí metody set_index.

zvirata = zvirata.set_index('id')

# Dataset obsahuje sloupec image_src, který má jako hodnoty odkazy na fotky jednotlivých zvířat.
# Například odkaz https://zoopraha.cz/images/lexikon-images/Drozd_oranIovohlav_.jpg vede na fotku drozda oranžovohlavého:
#
# Napiš funkci check_url, která bude mít jeden parametr radek.
# Funkce zkontroluje, jestli je odkaz v pořádku podle několika pravidel.
# K odkazu přistoupíš v těle funkce přes tečkovou notaci: radek.image_src.
# Zkontroluj následující:
# 1. datový typ je řetězec: isinstance(radek.image_src, str)
# 2. hodnota začíná řetězcem "https://zoopraha.cz/images/": radek.image_src.startswith("https://zoopraha.cz/images/")
# 3. hodnota končí buďto JPG nebo jpg.
# Zvol si jeden ze způsobů procházení tabulky, a na každý řádek zavolej funkci check_url.
# Pro každý řádek s neplatným odkazem vypiš název zvířete (title).

def check_url(radek):
    if isinstance(radek.image_src, str):
        if radek.image_src.startswith("https://zoopraha.cz/images/"):
            if radek.image_src.endswith(".jpg") or radek.image_src.endswith(".JPG"):
                pass
            else:
                print(radek['title'])
        else:
            print(radek['title'])
    else:
        print (radek['title'])

for id, zvire in zvirata.iterrows():
    check_url(zvire)