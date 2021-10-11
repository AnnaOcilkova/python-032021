import requests
import pandas
import numpy

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
    open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

castice = pandas.read_csv("air_polution_ukol.csv")

# Načti dataset a převeď sloupec date (datum měření) na typ datetime.

castice ['date'] = pandas.to_datetime(castice['date'])

# Přidej sloupce s rokem a číslem měsíce, které získáš z data měření.

castice['year'] = castice['date'].dt.year
castice['month'] = castice['date'].dt.month


# Vytvoř pivot tabulku s průměrným počtem množství jemných částic (sloupec pm25) v jednotlivých měsících a jednotlivých letech.
# Jako funkci pro agregaci můžeš použít numpy.mean.

castice_pivot = pandas.pivot_table(castice, values="pm25", index="year", columns="month", aggfunc=numpy.mean)
pandas.set_option('display.max_columns', None)


# Podívej se do první lekce na část o teplotních mapách a zobrat výsledek analýzy jako teplotní mapu.

# vizualizace grafů mi nefunguje, Jirka Pešík mi navrhl nějaké řešení, kdy se grafy alespoň ukládají do souboru, ale asi ho moc neumím používat

# Použij metodu dt.dayofweek a přidej si do sloupce den v týdnu.
# Číslování je od 0, tj. pondělí má číslo 0 a neděle 6.

castice['day_of_week'] = castice['date'].dt.dayofweek

# Porovnej, jestli se průměrné množství jemných částic liší ve všední dny a o víkendu.

castice['vikend/vsedni dny'] = numpy.where(castice["day_of_week"] < 5, 'vsedni dny', 'vikend')
castice_aggr = castice.groupby(["vikend/vsedni dny"])["pm25"].mean()
print(castice_aggr)
