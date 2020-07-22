# use least square method
from sklearn.linear_model import LinearRegression

linreg = LinearRegression()
linreg.fit(X_train, y_train)

print(linreg.intercept_)  # b
print(linreg.coef_)  # w

y_pred = linreg.predict(X_test)
