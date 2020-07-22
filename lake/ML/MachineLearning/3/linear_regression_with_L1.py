# Lasso      use Coordinate Descent
# LassoLars  use Least Angle Regression(LARS), same usage as Lasso
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=1)
lasso.fit(X_train, y_train)

print(lasso.intercept_)  # b
print(lasso.coef_)  # w

y_pred = lasso.predict(X_test)

# auto choose alpha

from sklearn.linear_model import LassoCV

lassocv = LassoCV(alphas=[0.01, 0.1, 0.5, 1, 3, 5, 7, 10, 20, 100])
lassocv.fit(X_train, y_train)
lassocv.alpha_  # best alpha
