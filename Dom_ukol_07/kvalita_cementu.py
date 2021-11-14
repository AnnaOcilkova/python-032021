import requests
import pandas
import seaborn
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/Concrete_Data_Yeh.csv")
with open("Concrete_Data_Yeh.csv", "wb") as f:
  f.write(r.content)

df = pandas.read_csv('Concrete_Data_Yeh.csv')

# V souboru Concrete_Data_Yeh.csv najdeš informace o kvalitě cementu.
# Sloupce 1-7 udávají množství jednotlivých složek v kg, které byly přimíchány do krychlového metru betonu (např. cement, voda, kamenivo, písek atd.).
# Ve sloupci 8 je stáří betonu a ve sloupci 9 kompresní síla betonu v megapascalech.
# Vytvoř regresní model, který bude predikovat kompresní sílu betonu na základě všech množství jednotlivých složek a jeho stáří.


mod = smf.ols(formula="csMPa ~ cement + slag + flyash + water + superplasticizer + coarseaggregate + fineaggregate + age", data=df)
res = mod.fit()
print(res.summary())

# Zhodnoť kvalitu modelu.

# R-squared: 0.616
# nepříliš přesný model

# Tipni si, která ze složek betonu ovlivňuje sílu betonu negativní (tj. má záporný regresní koeficient). Napiš, o kterou složku jde, do komentáře svého programu.

seaborn.heatmap(df.corr(), annot=True, linewidths=.5, fmt=".2f", cmap="Blues", vmax=1)
# plt.show()

# nejvíc negativně ovlivňuje sílu betonu množství vody