import yfinance as yf
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.ar_model import AutoReg
import pandas

# pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
# pandas.set_option('display.max_colwidth', 250)

# Pomocí modulu yfinance, který jsme používali v 5. lekci, stáhni ceny akcií společnosti Cisco (používají "Ticker" CSCO) za posledních 5 let.
# Dále pracuj s cenami akcie v závěru obchodního dne, tj. použij sloupec "Close".

csco = yf.Ticker("CSCO")
csco_df = csco.history(period="5y")
csco_df.describe()

# print(csco_df.head())

# Zobraz si graf autokorelace a podívej se, jak je hodnota ceny závislná na svých vlastních hodnotách v minulosti.

plot_acf(csco_df["Close"])
plt.show()

# Zkus použít AR model k predikci cen akcie na příštích 5 dní.
# Zobraz v grafu historické hodnoty (nikoli celou řadu, ale pro přehlednost např. hodnoty za posledních 50 dní) a tebou vypočítanou predikci.

model = AutoReg(csco_df['Close'], lags=50, trend="t", seasonal=False)
model_fit = model.fit()

predictions = model_fit.predict(start=csco_df.shape[0], end=csco_df.shape[0] + 4)
df_forecast = pandas.DataFrame(predictions, columns=["Prediction"])
df_with_prediction = pandas.concat([csco_df, df_forecast]).iloc[-55:]
df_with_prediction[["Close", "Prediction"]].plot()
plt.show()


