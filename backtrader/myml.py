from quantnoob.ml.linear_regression import LRM
from quantnoob.getdata import getPandaCsv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

ori_path = '/Users/ballmdr/blockchain-python/backtrader'
symbol = 'USDJPY'

X, y = getPandaCsv(ori_path=ori_path, symbol=symbol)
lrm = LRM(X, y)
lrm.train()
print(lrm.coef)
lrm.predict()

newdf = pd.DataFrame(lrm.coef, X.columns, columns=['Coef'])
print(newdf)
sns.scatterplot(lrm.y_test, lrm.predictions)

plt.show()