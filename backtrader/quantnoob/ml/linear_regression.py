from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

class LinearRegressionModel:

    def __init__(self, X_train, y_train, X_test, y_test):
        self.lm = LinearRegression()
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def train(self):
        self.lm.fit(self.X_train, self.y_train)
        self.coef = self.lm.coef_
    
    def predict(self):
        self.y_predict =  self.lm.predict(self.X_test)
        self.mse = mean_squared_error(self.y_test, self.y_predict)
        self.r2score = r2_score(self.y_test, self.y_predict)

    def live_predict(self, X_input):
        return self.lm.predict(X_input)