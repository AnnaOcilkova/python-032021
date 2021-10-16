
import requests
import pandas
import numpy

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/london_merged.csv")
open("london_merged.csv", 'wb').write(r.content)

kola = pandas.read_csv("london_merged.csv")

# Vytvoř sloupec, do kterého z časové značky (sloupec timestamp) ulož rok.
kola ['timestamp'] = pandas.to_datetime(kola['timestamp'])
kola['year'] = kola['timestamp'].dt.year

# Vytvoř kontingenční tabulku, která porovná kód počasí (sloupec weather_code se sloupcem udávající rok.
pandas.set_option('display.max_columns', None)
kola_pivot = pandas.pivot_table(kola, values="cnt", index="weather_code", columns="year", aggfunc=numpy.sum, margins = False)
print(kola_pivot)

# Jako hodnoty v kontingenční tabulce zobraz relativní počty jízd pro jednotlivé kódy počasí v jednom roce.
# Příklad možného výsledku by byl:
# v roce 2020 proběhlo 40 % jízd za počasí s kódem 1, 20 % jízd za počasí s kódem 2 a 40 % jízd za počasí s kódem 3 atd.
# Postup, jak na to, najdeš v v lekci v části označené jako "Čtení na doma".

kola_pivot_percentage = kola_pivot.div( kola_pivot.iloc[-1,:], axis=1)
print(kola_pivot_percentage)