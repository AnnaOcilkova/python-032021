import pandas
import requests

from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/soybean-2-rot.csv")
open("soybean-2-rot.csv", "wb").write(r.content)

# pandas.set_option('display.max_columns', None)
# pandas.set_option('display.max_rows', None)
# pandas.set_option('display.max_colwidth', 250)

# Rozhodovací strom nám umožňuje nahlédnout do pravidel, podle kterých postupuje ve klasifikaci. Díky tomu se často pokládá za velice průhledný nebo dobře interpretovatelný algoritmus.
# Podívej se na atribut feature_importances_ (clf.feature_importances_), který říká, které vstupní proměnné model použil pro rozhodování.
# Některé budou mít nulovou hodnotu, to znamená, že vůbec potřeba nejsou. Atribut nám dá jen seznam čísel seřazený podle vstupních proměnných, ale ne jejich jména.
# Ty získáš například z OneHotEncoder (atribut feature_names_in_, takže například níže by se jednalo o oh_encoder.feature_names_in_,
# případně můžeš také použít místo atributu feature_names_in_ metodu get_feature_names())
# Která vstupní proměnná má největší "důležitost"?
# Stačí nám tato proměnná pro úspěšnou klasifikaci? Jaký je rozdíl mezi hodnotou f1_score při použití všech proměnných a jen této jedné "nejdůležitější" proměnné?

data = pandas.read_csv("soybean-2-rot.csv")
# print(data.columns)
X = data.drop(columns=["class"])
# X = data["plant-stand"]
input_features = X.columns  # Ulozime si nazvy sloupcu/promennych
y = data["class"]
# print(X)

oh_encoder = OneHotEncoder()
X = oh_encoder.fit_transform(X)

fn = pandas.DataFrame(oh_encoder.get_feature_names(input_features=input_features)).reset_index()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

clf = DecisionTreeClassifier(max_depth=3, min_samples_leaf=1)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(f1_score(y_test, y_pred, average='weighted'))
# print(f1_score(y_test, y_pred, average=None)) špatně, tohle vyhodí výsledek pro 3 hodnoty y proměnné, ne pro x


fi = pandas.DataFrame(clf.feature_importances_).reset_index()
f = pandas.merge(fn, fi, on=['index']).sort_values(by='0_y', ascending=False)
print(f)

# největší důležitost má proměnná plant-stand

# s úpravou modelu pro použití pouze jedné proměnné jsem si bohužel neporadila...

# pipeline - https://scikit-learn.org/stable/tutorial/statistical_inference/putting_together.html