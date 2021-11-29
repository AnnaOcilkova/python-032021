import pandas
import requests
import matplotlib.pyplot as plt

from sklearn.metrics import (
    f1_score,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Stáhni si dataset kosatce.csv, který obsahuje pozorování o dvou typech kosatce.
# Jako vstupní proměnné pro předpověď typu kosatce ( Setosa a Virginica) máme délku kalichu a délku okvětního lístku.
# Výstupní proměnná je označená jako target.
#
# Načti si data do proměnných X a y

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/kosatce.csv")
open("kosatce.csv", "wb").write(r.content)

data = pandas.read_csv("kosatce.csv")
# print(data.isna().sum())

X = data.drop(columns=["target"])
y = data["target"]

# Rozděl data na trénovací a testovací
# (velikost testovacích dat nastav na 30% a nezapomeň nastavit proměnnou random_state, aby tvoje výsledky byly reprodukovatelné)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Pokud použijeme stejný algoritmus jako v prvním úkolu, tj. KNeighborsClassifier,
# je možné předpovědět typ kosatce na základě těchto dat tak, aby metrika f1_score dosáhla alespoň 85%?

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

ks = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
f1_scores = []

for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    f1_scores.append(f1_score(y_test, y_pred))

plt.plot(ks, f1_scores)
plt.axhline(y=0.85, color = 'red')
# plt.plot(ks, 0.85)
plt.show()

# Pokud použijeme stejný algoritmus jako v prvním úkolu, tj. KNeighborsClassifier,
# je možné předpovědět typ kosatce na základě těchto dat tak, aby metrika f1_score dosáhla alespoň 85%?

# ano, je , například pro ks = 15, 17 atd. (viz graf, vse nad cervenou carou)

clf = KNeighborsClassifier(n_neighbors=15)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(f1_score(y_test, y_pred))