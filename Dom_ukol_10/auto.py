import pandas
import requests
import matplotlib.pyplot as plt

from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV

r = requests.get(
    "https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/auto.csv"
)
open("auto.csv", "wb").write(r.content)

pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
# pandas.set_option('display.max_colwidth', 250)

# Pracuj se souborem auto.csv. Obsahuje informace o vyráběných modelech aut mezi lety 1970-1982.
#
# Načti data. Při volání metody read_csv nastav parametr na_values: na_values=["?"].
# Neznámé/prázdné hodnoty jsou totiž reprezentované jako znak otazníku.
# Po načtení dat se zbav řádek, které mají nějakou neznámou/prázdnou hodnotu (nápověda: dropna).

data = pandas.read_csv("auto.csv", na_values=["?"])
data = data.dropna()
# print(data.head(150))

# Naše výstupní proměnná bude sloupec "origin". Pod kódy 1, 2 a 3 se skrývají regiony USA, Evropa a Japonsko.
# Zkus odhadnout (třeba pomocí sloupce "name"), který region má který kód :-)

# 1-USA, 2-Evropa, 3-Japonsko

# Podívej se, jak se měnila spotřeba aut v letech 1970-1982.
# Vytvoř graf, který ukáže průměrnou spotřebu v jednotlivých letech (graf může být sloupcový nebo čarový,
# a může ukazovat celkovou průměrnou spotřebu, nebo, jako dobrovolný doplněk, zobraz spotřebu tak, aby byly rozlišené tři regiony).

data_grouped = data.groupby('year')['mpg'].mean().reset_index()
data_grouped.plot(kind="bar", x='year', y='mpg')
# plt.show()

# Rozděl data na vstupní a výstupní proměnnou, a následně na trénovací a testovací sadu v poměru 70:30.

X = data.drop(columns=["origin", 'name'])
y = data["origin"]

# encoder = OneHotEncoder()
# X = encoder.fit_transform(X['name'])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42)

# Data normalizuj:

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Použij klasifikační algoritmus rozhodovacího stromu, a vyber jeho parametry technikou GridSearchCV:
# Jaké jsi dosáhl/a metriky f1_score?

model = DecisionTreeClassifier(random_state=0)
clf = GridSearchCV(model, param_grid={'max_depth': [1,3,5,7,9,11,13,15,17,19], 'min_samples_leaf': [1,3,5,7,9,11,13,15,17,19]})
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(clf.best_params_)
print(f1_score(y_test, y_pred, average='weighted'))








