import requests
import pandas
import numpy


r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/titanic.csv")
open("titanic.csv", 'wb').write(r.content)


# Titanic
# V souboru titanic.csv najdeš informace o cestujících na zaoceánském parníku Titanic.
# Vytvoř kontingenční tabulku, která porovná závislost mezi pohlavím cestujícího (soupec Sex),
# třídou (sloupec Pclass), ve které cestoval, a tím, jesti přežil potopení Titanicu (sloupec Survived).
# Pro data můžeš použít agregaci len, numpy.sum, která ti spočte absolutní počet přeživších pro danou kombinaci,
# nebo numpy.mean, která udá relativní počet přeživších pro danou kombinaci.

cestujici = pandas.read_csv("titanic.csv")
# print (cestujici.columns.values)

cestujici_pivot = pandas.pivot_table(cestujici, values="Survived", index="Sex", columns="Pclass", aggfunc=numpy.sum)
print(cestujici_pivot)

# Z dat vyfiltruj pouze cestující, kteří cestovali v první třídě.
# Dále použij metodu cut na rozdělení cestujících do věkových skupin (zkus vytvořit např. 4 skupiny,
# můžeš definovat hranice skupin tak, aby vznikly skupiny děti, teenageři, dospělí a senioři).
# Urči relativní počet přeživších pro jednotlivé kombinace pohlavní a věkové skupiny.

cestujici_1 = cestujici[cestujici['Pclass'] == 1]
cestujici_1 = cestujici_1.drop(['Siblings/Spouses Aboard', 'Name', 'Pclass', 'Parents/Children Aboard', 'Fare'], 1)

cestujici_1['kategorie'] = pandas.cut(x=cestujici_1['Age'], bins=[0, 9, 17, 60, 110], labels=['Deti', 'Teenageri', 'Dospeli', 'Seniori'])
#  pandas.set_option('display.max_rows', None)

cestujici_1_pivot = pandas.pivot_table(cestujici_1, values="Survived", index="Sex", columns="kategorie", aggfunc=numpy.sum)
print(cestujici_1_pivot)