# use least square method
from sklearn.linear_model import Ridge

ridge = Ridge(alpha=1)
ridge.fit(X_train, y_train)

print(ridge.intercept_)  # b
print(ridge.coef_)  # w

y_pred = ridge.predict(X_test)

# auto choose alpha

from sklearn.linear_model import RidgeCV

ridgecv = RidgeCV(alphas=[0.01, 0.1, 0.5, 1, 3, 5, 7, 10, 20, 100])
ridgecv.fit(X_train, y_train)
ridgecv.alpha_  # best alpha
