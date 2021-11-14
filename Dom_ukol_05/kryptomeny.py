import requests
import pandas
import seaborn
import matplotlib.pyplot as plt

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/crypto_prices.csv")
open("crypto_prices.csv", "wb").write(r.content)

prices = pandas.read_csv("crypto_prices.csv")

# pandas.set_option('display.max_columns', None)
# pandas.set_option('display.max_rows', None)
# pandas.set_option('display.max_colwidth', 250)

# V souboru crypto_prices.csv najdeš ceny různých kryptoměn v průběhu času. Datum je ve sloupci Date a název kryptoměny ti prozradí sloupec Name,
# alternativně můžeš využít sloupec Symbol.
#
# Použij zavírací cenu kryptoměny (sloupec Close) a vypočti procentuální změnu jednotlivých kryptoměn.

prices['Pct_change'] = prices.groupby('Symbol')['Close'].pct_change()




# prices_red = prices[['Symbol', 'Date', 'Pct_change']]
# print(prices.head(278))

# prices_grouped = prices.groupby('Name').sum


# Pozor na to, ať se ti nepočítají ceny mezi jednotlivými měnami. Ošetřit to můžeš pomocí metody groupby(), jako jsme to dělali např. u metody shift().
# Vytvoř korelační matici změn cen jednotlivých kryptoměn a zobraz je jako tabulku.

prices_corr = prices['Pct_change'].corr()

# print(prices_corr())

# seaborn.heatmap(prices.corr(), annot=True, linewidths=.5, fmt=".2f", cmap="Blues", vmax=1)
# plt.show()


# V tabulce vyber dvojici kryptoměn s vysokou hodnotou koeficientu korelace a jinou dvojici s koeficientem korelace blízko 0.
# Změny cen pro dvojice měn, které jsou nejvíce a nejméně korelované, si zobraz jako bodový graf.
# Takto nějak by měla vypadat korelační matice, ke které dojdeš.