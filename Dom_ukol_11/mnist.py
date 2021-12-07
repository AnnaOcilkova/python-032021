import pandas
import requests

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.datasets import load_digits

# Načti data do proměnné X:

digits = load_digits()
X = digits.data

# Data normalizuj

scaler = StandardScaler()
X = scaler.fit_transform(X)

# Redukuj počet vstupních proměnných na dvě pomocí TSNE. Můžeš vyzkoušet různé parametry.

tsne = TSNE(
    init="pca",
    n_components=2,
    perplexity=20,
    learning_rate="auto",
    random_state=0,
)
X = tsne.fit_transform(X)

# Vykresli data do bodového grafu. Kolik odhaduješ shluků (clusterů)?

plt.scatter(X[:, 0], X[:, 1], s=50)
# plt.show()

# odhaduji 11 shluků

# Aplikuj algoritmus KMeans s počtem shluků, který jsi odhadl/a v předchozím kroku

model = KMeans(n_clusters=11, random_state=0)
labels = model.fit_predict(X)

plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap="Set1")
centers = model.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c="black", s=200, alpha=0.5)
# plt.show()

# Vyhodnoť výsledek pomocí silhouette_score, který by měl být alespoň 0.5

print(silhouette_score(X, labels))