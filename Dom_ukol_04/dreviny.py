import pandas
import numpy
import seaborn as sns
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

HOST = "czechitaspsql.postgres.database.azure.com"
PORT = 5432
USER = "anna.ocilkova"
USERNAME = f"anna.ocilkova@czechitaspsql"
DATABASE = "postgres"
PASSWORD = "YgW4TIZNB0aMZa5U"
engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=False)

pandas.set_option('display.max_columns', None)
# pandas.set_option('display.max_rows', None)
# pandas.set_option('display.max_colwidth', 250)

# Pomocí SQL dotazu do databáze si připrav dvě pandas tabulky:
# tabulka smrk bude obsahovat řádky, které mají v sloupci dd_txt hodnotu "Smrk, jedle, douglaska"
# tabulka nahodila_tezba bude obsahovat řádky, které mají v sloupci druhtez_txt hodnotu "Nahodilá těžba dřeva"

smrk = pandas.read_sql("SELECT * from \"dreviny\" WHERE dd_txt = 'Smrk, jedle, douglaska'", con=engine)
nahodila_tezba = pandas.read_sql("SELECT * from \"dreviny\" WHERE druhtez_txt = 'Nahodilá těžba dřeva'", con=engine)

# Vytvoř graf, který ukáže vývoj objemu těžby pro tabulku smrk. Pozor, řádky nemusí být seřazené podle roku.

smrk.sort_values(by="rok").plot.bar(x="rok", y="hodnota", title="Vývoj objemu těžby dřeva -Smrk, jedle, douglaska")
plt.show()

# Vytvoř graf (nebo několik grafů), který ukáže vývoj objemu těžby v čase pro všechny typy nahodilé těžby. Můžeš použít vlastní postup, nebo postupuj podle jedné z nápověd:
# První metoda: agreguj tabulku nahodila_tezba pomocí metody pivot_table a na výsledek zavolej metodu plot().
# Druhá metoda: agreguj tabulku nahodila_tezba pomocí metody groupby a na výsledek zavolej metodu plot(), kde specifikuješ, který sloupec bude na ose x, a který na ose y.

nahodila_tezba_pivot = pandas.pivot_table(nahodila_tezba, values="hodnota", index="rok", columns="prictez_txt", aggfunc=numpy.sum, margins = False)

sns.lineplot(data=nahodila_tezba_pivot["Exhalační příčina"])
sns.lineplot(data=nahodila_tezba_pivot["Hmyzová příčina"])
sns.lineplot(data=nahodila_tezba_pivot["Příčina jiná než živelní, exhalační a hmyzová"])
sns.lineplot(data=nahodila_tezba_pivot["Živelní příčina"])

plt.legend(['Exhalační příčina', "Hmyzová příčina", "Příčina jiná než živelní, exhalační a hmyzová", "Živelní příčina"])
plt.xlabel('rok')
plt.ylabel('objem těžby')

plt.show()

# můžu se zeptat jak bych upravila legendu osy x aby tam nebyla ta desetinná čísla? převést roky na jiný datový typ?


# Koment lektorky
# Pomocí sns jsem si zkusila ještě jedno řešení s parametrem hue:
# sns.lineplot(data=nahodila_tezba, x='rok', y='hodnota', hue='prictez_txt')
# Případně pomocí pivot_table:
# pandas.pivot_table(nahodila_tezba, values="hodnota", index="rok", columns="prictez_txt", aggfunc=numpy.sum, margins = False).plot()