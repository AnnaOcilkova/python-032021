import requests
import pandas
import seaborn
import matplotlib.pyplot as plt

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/crypto_prices.csv")
open("crypto_prices.csv", "wb").write(r.content)

prices = pandas.read_csv("crypto_prices.csv")

# V souboru crypto_prices.csv najdeš ceny různých kryptoměn v průběhu času. Datum je ve sloupci Date a název kryptoměny ti prozradí sloupec Name,
# alternativně můžeš využít sloupec Symbol.
#
# Použij zavírací cenu kryptoměny (sloupec Close) a vypočti procentuální změnu jednotlivých kryptoměn.
# Pozor na to, ať se ti nepočítají ceny mezi jednotlivými měnami. Ošetřit to můžeš pomocí metody groupby(), jako jsme to dělali např. u metody shift().

prices['Pct_change'] = prices.groupby('Symbol')['Close'].pct_change()

# Vytvoř korelační matici změn cen jednotlivých kryptoměn a zobraz je jako tabulku.

prices_pivot = pandas.pivot(prices, values='Pct_change', index='Date', columns='Symbol')
prices_pivot_corr = prices_pivot.corr()

# V tabulce vyber dvojici kryptoměn s vysokou hodnotou koeficientu korelace a jinou dvojici s koeficientem korelace blízko 0.

# vysoká korelace - WBTC vs BTC
# nízká korelace - XMR vs USDT

# Změny cen pro dvojice měn, které jsou nejvíce a nejméně korelované, si zobraz jako bodový graf.

seaborn.scatterplot(x="WBTC", y="BTC", data=prices_pivot_corr, color='blue')
seaborn.scatterplot(x="XMR", y="USDT", data=prices_pivot_corr, color='red')
plt.show()