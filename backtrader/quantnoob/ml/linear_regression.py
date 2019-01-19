from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class LRM:

    def __init__(self, X, y):
        self.lm = LinearRegression()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3, random_state=101)

    def train(self):
        self.lm.fit(self.X_train, self.y_train)
        self.coef = self.lm.coef_
    
    def predict(self):
        self.predictions =  self.lm.predict(self.X_test)