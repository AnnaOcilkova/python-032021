import pandas
import requests
import seaborn
import matplotlib.pyplot as plt

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/Fish.csv")
with open("Fish.csv", "wb") as f:
  f.write(r.content)

df = pandas.read_csv('Fish.csv')

# V souboru Fish.csv najdeš informace o rybách z rybího trhu:
# délku (vertikální - Length1, diagonální - Length2 a úhlopříčnou - Length3),výšku,šířku,živočišný druh ryby,hmnotnost ryby.
# Vytvoř regresní model, který bude predikovat hmnotnost ryby na základě její diagonální délky (sloupec Length2).

import statsmodels.formula.api as smf

mod = smf.ols(formula="Weight ~ Length2", data=df)
res = mod.fit()
# print(res.summary())

# Zkus přidat do modelu výšku ryby (sloupec Height) a porovnej, jak se zvýšila kvalita modelu.

mod2 = smf.ols(formula="Weight ~ Length2 + Height", data=df)
res2 = mod2.fit()
# print(res2.summary())

# koeficient determinace se zvýšil z 0.844 na 0.875 (vysvětlili jsme o 3.1% rozptylu hodnot více)

# Nakonec pomocí metody target encoding zapracuj do modelu živočišný druh ryby.

prumery = df.groupby('Species')['Weight'].mean()
df['druh_prum_vaha'] = df['Species'].map(prumery)

mod3 = smf.ols(formula="Weight ~ Length2 + Height + druh_prum_vaha", data=df)
res3 = mod3.fit()
# print(res3.summary())

# koeficient determinace se zvýšil na 0.9