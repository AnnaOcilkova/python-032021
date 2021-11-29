import pandas
import requests
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    ConfusionMatrixDisplay,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV


r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/water-potability.csv")
open("water-potability.csv", 'wb').write(r.content)

data = pandas.read_csv("water-potability.csv")
# print(data.shape)

# Zopakuj experiment, ale tentokrát vyber hodnotu parametru n_neighbors na základě metriky precision.
# Znamená to, že pro nás bude důležité, abychom raději označili pitnou vodu za nepitnou, než nepitnou za pitnou.
# Raději nebudeme pít vůbec, než abychom se napili nepitné vody a onemocněli.
# V podstatě bude potřeba upravit krok 6. Upravení parametrů modelu.
# Na základě číselných hodnot nebo grafu vyber tu hodnotu parametru, která dává nejlepší výsledek (nejvyšší hodnotu při volání precision()).

# print(data.isna().sum())
data = data.dropna()

# print(data["Potability"].value_counts(normalize=True))   # zjistit rozdělení obou možností pitelnosti

X = data.drop(columns=["Potability"])
y = data["Potability"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


ks = [71, 83, 85, 87, 89, 91, 93, 95, 201]
precision_scores = []

for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    precision_scores.append(precision_score(y_test, y_pred))

# plt.plot(ks, precision_scores)
# plt.show()

clf_final = KNeighborsClassifier(n_neighbors=89)
clf_final.fit(X_train, y_train)
y_pred = clf_final.predict(X_test)
print(f'precision score pro k = 89: {precision_score(y_test, y_pred)}')


# Liší se tvůj zvolený parametr od parametru, který jsme jako závěrečný zvolili v lekci?

# ano, liší
# v lekci k = 3
# nyní mi vyšlo nejlepší k = 89


# Jak vypadá matice chyb (confusion matrix)? Dovedeš z matice odvodit výpočet, který nám dá stejnou hodnotu, jako při použití metody precision()?

ConfusionMatrixDisplay.from_estimator(
    clf_final,
    X_test,
    y_test,
    display_labels=clf_final.classes_,
    cmap=plt.cm.Blues,
)
plt.show()

# zjišťujeme poměr správně odhadnutých pitných vzorků (pravý dolní roh) ku všem o kterých odhadujeme, že jsou pitné (celý pravý sloupec)


