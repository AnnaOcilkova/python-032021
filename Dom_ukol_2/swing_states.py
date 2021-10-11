import requests
import pandas
import numpy

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/1976-2020-president.csv") as r:
  open("1976-2020-president.csv", 'w', encoding="utf-8").write(r.text)

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
  open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

president_elections = pandas.read_csv("1976-2020-president.csv")

# Urči pořadí jednotlivých kandidátů v jednotlivých státech a v jednotlivých letech (pomocí metody rank()).
# Nezapomeň, že data je před použitím metody nutné seřadit a spolu s metodou rank() je nutné použít metodu groupby().

president_elections = president_elections.sort_values(['year', 'state', 'candidatevotes'], ascending=True)
president_elections["rank"] = president_elections.groupby(["year",'state'])["candidatevotes"].rank(method="min", ascending=False)
# pandas.set_option('display.max_columns', None)
# pandas.set_option('display.max_rows', None)

# Pro další analýzu jsou důležití pouze vítězové. Ponech si v tabulce pouze řádky, které obsahují vítěze voleb v jednotlivých letech v jednotlivých státech.

vitezove = president_elections[president_elections['rank'] == 1]

# Pomocí metody shift() přidej nový sloupec, abys v jednotlivých řádcích měl(a) po sobě vítězné strany ve dvou po sobě jdoucích letech.

vitezove = vitezove.sort_values(['state', 'year'], ascending=True)

# Porovnej, jestli se ve dvou po sobě jdoucích letech změnila vítězná strana. Můžeš k tomu použít např. funkce numpy.where a vložit hodnotu 0 nebo 1 podle toho, jestli došlo ke změně vítězné strany.

vitezove["previous_winner"] = vitezove["party_simplified"].shift(periods=1)
vitezove["changed_winner_party"] = numpy.where(vitezove["party_simplified"] == vitezove["previous_winner"], 0, 1)

# Proveď agregaci podle názvu státu a seřaď státy podle počtu změn vítězných stran.

vitezove_grouped = pandas.DataFrame(vitezove.groupby(["state"])['changed_winner_party'].sum())
vitezove_grouped = vitezove_grouped.sort_values(['changed_winner_party'], ascending=False)
print(vitezove_grouped.head())

# U amerických voleb je zajímavý i tzv. margin, tedy rozdíl mezi prvním a druhým kandidátem.
# Přidej do tabulky sloupec, který obsahuje absolutní rozdíl mezi vítězem a druhým v pořadí. Nezapomeň, že je k tomu potřeba kompletní dataset, tj. je potřeba tabulku znovu načíst, protože v předchozí části jsme odebrali některé řádky.
# Můžeš přidat i sloupec s relativním marginem, tj. rozdílem vyděleným počtem hlasů.
# Seřaď tabulku podle velikosti margin (absolutním i relativním) a zjisti, kde byl výsledek voleb nejtěsnější.

president_elections = president_elections.sort_values(['state', 'year', 'rank'], ascending=True)
president_elections["second_candidate_votes"] = president_elections["candidatevotes"].shift(periods=-1)
president_elections["margin_absolute"] = president_elections['candidatevotes'] - president_elections['second_candidate_votes']
president_elections["margin_relative"] = (president_elections['candidatevotes'] - president_elections['second_candidate_votes']) / president_elections["totalvotes"]
president_elections_winners = president_elections[president_elections['rank'] == 1]
president_elections_winners = president_elections_winners.sort_values(['margin_absolute'], ascending=False)
print(president_elections_winners)
president_elections_winners = president_elections_winners.sort_values(['margin_relative'], ascending=False)
print(president_elections_winners)