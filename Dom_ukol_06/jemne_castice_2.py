import requests
import pandas

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
  open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

castice = pandas.read_csv("air_polution_ukol.csv")

# pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
# pandas.set_option('display.max_colwidth', 250)

# V souboru air_polution_ukol.csv najdeš data o množství jemných částic změřených v ovzduší v jedné plzeňské meteorologické stanici a který jsme již používali v úkolu z druhého týdne.
# Pokud máš úkol hotový, můžeš si z něj zkopírovat následující krok:
# Načti dataset a převeď sloupec date (datum měření) na typ datetime.

castice['date'] = pandas.to_datetime(castice['date'])
# castice = castice.dropna()

# Dále pokračuj následujícími kroky:
#
# Z dat vyber data za leden roku 2019 a 2020.

castice_vyber = castice[(castice['date'].dt.month == 1)]
castice_vyber = castice_vyber[(castice_vyber['date'].dt.year == 2019) | (castice_vyber['date'].dt.year == 2020)]


# Porovnej průměrné množství jemných částic ve vzduchu v těchto dvou měsících pomocí Mann–Whitney U testu.
# Formuluj hypotézy pro oboustranný test (nulovou i alternativní) a napiš je do komentářů v programu.
# Měl(a) bys dospět k výsledku, že p-hodnota testu je 1.1 %.

# 1. průměrné množství jemných částic v 01/2019 a 01/2020 je stejné
# 2. průměrné množství jemných částic v 01/2019 a 01/2020 se liší

from scipy.stats import mannwhitneyu

castice_vyber['year'] = castice_vyber['date'].dt.year
castice_vyber = castice_vyber.set_index("year")

x = castice_vyber.loc[2019, 'pm25']
y = castice_vyber.loc[2020, 'pm25']
print(mannwhitneyu(x, y, alternative = 'two-sided'))

# Rozhodni, zda bys na hladině významnosti 5 % zamítla nulovou hypotézu. Své rozhodnutí napiš do programu

# P-hodnota je nizsi nez hladina vyznamnosti, nulovou hypotezu tedy zamitame.