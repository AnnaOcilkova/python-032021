import requests
import pandas
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/MLTollsStackOverflow.csv")
with open("MLTollsStackOverflow.csv", "wb") as f:
  f.write(r.content)

questions = pandas.read_csv("MLTollsStackOverflow.csv")

# pandas.set_option('display.max_columns', None)
# pandas.set_option('display.max_rows', None)
# pandas.set_option('display.max_colwidth', 250)

# Stáhni si soubor MLTollsStackOverflow.csv, který obsahuje počty položených otázek na jednotlivé programovací techniky a další technologie.
# Vyber sloupec python.
# Proveď dekompozici této časové řady pomocí multiplikativního modelu. Dekompozici zobraz jako graf.

decompose = seasonal_decompose(questions['python'], model='multiplicative', period=12)
# decompose.plot()
# plt.show()

# Vytvoř predikci hodnot časové řady pomocí Holt-Wintersovy metody na 12 měsíců.
# Sezónnost nastav jako 12 a uvažuj multiplikativní model pro trend i sezónnost. Výsledek zobraz jako graf.

mod = ExponentialSmoothing(questions["python"], seasonal_periods=12, trend="mul", seasonal="mul", use_boxcox=True, initialization_method="estimated",)
res = mod.fit()
questions["HM"] = res.fittedvalues
# questions[["HM", "python"]].plot()

questions_forecast = pandas.DataFrame(res.forecast(12), columns=["Prediction"])
questions_with_prediction = pandas.concat([questions, questions_forecast])
questions_with_prediction[["python", "Prediction"]].plot()
plt.show()