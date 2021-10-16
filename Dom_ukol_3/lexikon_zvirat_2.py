import requests
import pandas
import numpy

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/lexikon-zvirat.csv")
open("lexikon-zvirat.csv", "wb").write(r.content)

zvirata = pandas.read_csv("lexikon-zvirat.csv", sep = ';')
# pandas.set_option('display.max_columns', None)
# pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_colwidth', 250)


zvirata = zvirata.dropna(axis=0, how='all')
zvirata = zvirata.dropna(axis=1, how='all')

# Chceme ke každému zvířeti vytvořit popisek na tabulku do zoo.
# Popisek bude využívat sloupců title (název zvířete), food (typ stravy), food_note (vysvětlující doplněk ke stravě) a description (jak zvíře poznáme).
# Napiš funkci popisek, která bude mít jeden parametr radek. Funkce spojí informace dohromady.
# Následně použijte metodu apply, abyste vytvořili nový sloupec s tímto popiskem.

def popisek (radek):
    title = zvirata.title
    food = zvirata.food
    food_note = zvirata.food_note
    description = zvirata.description
    popis = (f'  {radek.title} preferuje následující typ stravy: {radek.food}. Konkrétně ocení když mu do misky přistanou {radek.food_note}.\n  Jak toto zvíře poznáme: {radek.description}')
    return popis

zvirata["popisek"] = zvirata.apply(popisek, axis=1)
print (zvirata[['title', 'popisek']])

# DOTAZ - když jsem zavolala funkci jinak (třeba cyklem for), zalomení řádku \n v textu se zobrazilo. Proč se nezobrazí při tomto použití a vypíše zalomení jen jako další text '\n'?

