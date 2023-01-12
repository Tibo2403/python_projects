import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as ss

n = 500
beta_0 = 5
beta_1 = 2
beta_2 = -1
np.random.seed(1)
x_1 = 10 * ss.uniform.rvs(size=n)
x_2 = 10 * ss.uniform.rvs(size=n)
y = beta_0 + beta_1 * x_1 + beta_2 * x_2 + ss.norm.rvs(loc=0, scale = 1, size = n)
X = np.stack([x_1, x_2], axis=1)

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:,0], X[:,1], y, c=y)
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.set_zlabel("$y$")

from sklearn.linear_model import LinearRegression
lm = LinearRegression(fit_intercept=True)
lm.fit(X, y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size= 0.5, random_state=1 )
lm = LinearRegression(fit_intercept=True)
lm.fit(X_train, y_train)

h = 1
sd = 1
n = 50
def gen_data(n, h, sd1, sd2):
    x1 = ss.norm.rvs(-h, sd1, n)
    y1 = ss.norm.rvs(0, sd1, n)
    x2 = ss.norm.rvs(h, sd2, n)
    y2 = ss.norm.rvs(0, sd2, n)
    return (x1, y1, x2, y2)
(x1, y1, x2, y2) = gen_data(50, 1.5, 1, 1.5)
(x1, y1, x2, y2) = gen_data(1000, 0, 1, 1)
(x1, y1, x2, y2) = gen_data(1000, 1, 2, 2.5)
(x1, y1, x2, y2) = gen_data(1000, 10, 100, 100)
(x1, y1, x2, y2) = gen_data(1000, 20, .5, .5)

def plot_data(x1, y1, x2, y2):
    plt.figure()
    plt.plot(x1, y1, "o", ms=2)
    plt.plot(x2, y2, "o", ms=2)
    plt.xlabel("$X_1$")
    plt.ylabel("$X_2$")