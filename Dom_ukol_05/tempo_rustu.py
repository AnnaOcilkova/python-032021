import requests
import pandas
import statistics


r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/crypto_prices.csv")
open("crypto_prices.csv", "wb").write(r.content)

prices = pandas.read_csv("crypto_prices.csv")
prices_pivot = pandas.pivot(prices, values='Close', index='Date', columns='Symbol')
# print(prices_pivot.head())

# pandas.set_option('display.max_columns', None)
# pandas.set_option('display.max_rows', None)
# pandas.set_option('display.max_colwidth', 250)

# Z datového souboru si vyber jednu kryptoměnu a urči průměrné denní tempo růstu měny za sledované období.
# Můžeš využít funkci geometric_mean z modulu statistics.

prices_XMR = prices[prices['Symbol'] == 'XMR']
# print(statistics.geometric_mean(prices_XMR['Close']))


# Vyber si sloupec se změnou ceny, kterou máš vypočítanou z předchozího cvičení (případně si jej dopočti),
# přičti k němu 1 (nemusíš dělit stem jako v lekci, hodnoty jsou jako desetinná čísla, nikoli jako procenta) a převeď jej na seznam pomocí metody .tolist().

prices_XMR['Pct_change'] = prices_XMR.groupby('Symbol')['Close'].pct_change() + 1
prices_XMR_list = prices_XMR['Pct_change'].dropna().tolist()

# Následně vypočti geometrický průměr z těchto hodnot.

print(statistics.geometric_mean(prices_XMR_list)-1)

# Např. pro měnu XMR (Monero) vychází průměrný mezidenní růst ceny na 0.001794558895.