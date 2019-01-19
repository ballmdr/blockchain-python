from quantnoob.ml.linear_regression import LinearRegressionModel
from quantnoob.getdata import getPandaCsv, getTrainTest, getDateRange
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

ori_path = '/Users/ballmdr/blockchain-python/backtrader'
symbols = ['NZDUSD', 'EURUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'GBPUSD', 'AUDUSD', 'AUDCHF', 'NZDJPY', 'CADJPY', 'AUDJPY', 'EURJPY']
X_columns = ['open', 'high', 'low', 'close', 'volume']
y_columns = 'close'


result = pd.DataFrame(columns=['symbol', 'MSE', 'r2score'])

for symbol in symbols:

    df = getPandaCsv(ori_path=ori_path, symbol=symbol)
    trainfrom = datetime(2011,1,1)
    trainto = datetime(2016,12,31)
    testfrom = datetime(2017,1,1)
    testto = datetime(2018,12,31)

    X_train, y_train, X_test, y_test = getTrainTest(df=df, trainfrom=trainfrom, trainto=trainto, testfrom=testfrom, testto=testto, X_columns=X_columns, y_columns=y_columns)

    lrm = LinearRegressionModel(X_train, y_train, X_test, y_test)
    lrm.train()
    lrm.predict()

    result = result.append({'symbol': symbol, 'MSE': lrm.mse, 'r2score': lrm.r2score}, ignore_index=True)

    sns.scatterplot(lrm.y_test, lrm.y_predict)
# plt.show()
# plt.plot(lrm.y_predict)
# plt.show()

plt.legend()
plt.show()
print(result.sort_values(by=['MSE'], ascending=True))

# fromdate = datetime(2019,1,8)
# todate = datetime(2019,1,9)
# price_today = getDateRange(df, fromdate, todate)[X_columns]
# close_tommorow = lrm.live_predict(price_today)


