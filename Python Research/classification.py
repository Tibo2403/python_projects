import random

def majority_vote(votes):
    """xxx"""
    vote_counts = {}
    for vote in votes:
        if vote in vote_counts:
            vote_counts[vote] += 1
        else:
            vote_counts[vote] = 1
    winners = []
    max_count = max(vote_counts.values())
    for vote, count in vote_counts.items():
        if count == max_count:
            winners.append(vote)
        # print(vote, count)
    return random.choice(winners)

votes = [1,2,3,1,2,3,1,2,3,3,3,3]
vote_counts = majority_vote(votes)

def distance(p1,p2):
    """Finds the distance between points p1 and p2."""
    return np.sqrt(np.sum(np.power(p2 - p1,2)))
import numpy as np
p1 = np.array([1,1])
p2 = np.array([4,4])
distance(p1,p2)

import scipy.stats as ss
def majority_vote_short(votes):
    """Return the most common element in vote"""
    mode, count = ss.mstats.mode(votes)
    return mode

import numpy as np
points = np.array([1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3])
p = np.array([2.5, 2])

import matplotlib.pyplot as plt
plt.plot(points[:,0], points[:,1], "ro")
plt.plot(p[0], p[1], "bo")
plt.axis([0.5, 3.5, 0.5, 3.5])

def find_nearest_neighbors(p, points, k=5):
    """Find the k nearest neighbors of point p and return their indices."""
    distances = np.zeros(points.shape[0])
    for i in range(len(distances)):
        distances[i] = distance(p, points[i])
    np.argsort(distances)
    return ind[:k]

ind = find_nearest_neighbors(p, points, 2); print[ind]
def knn_predict(p, points,outcomes, k=5):
    # find k nearest neighbors
    ind = find_nearest_neighbors(p, points, k)
    return majority_vote(outcomes[ind])
    # predict the class of p based on majority vote

outcomes = np.array([0,0,0,0,1,1,1,1,1])
def genereate_synth_data(n=50):
    """Create two sets of points from bivariate normal distribution."""
    points = np.concatenate(ss.norm(0,1).rvs((n,2)),ss.norm(1,1).rvs((n,2)), axis=0)
    outcomes = np.concatenate((np.repeat(0,n), np.repeat(1,n)))
    return (points, outcomes)
n = 20
plt.figure()
plt.plot(points[:n,0], points[:n,1], "ro")
plt.plot(points[n:,0], points[n:,1], "bo")
plt.savefig("bivardata.pdf")

def make_prediction_grid(predictors, outcomes, limits, h, k):
    """Classify each point on the prediction grid."""
    (x_min, x_max, y_min, y_max) = limits
    xs = np.arrange(x_min, x_max, h)
    ys = np.arrange(y_min, y_max, h)
    xx, yy = np.meshgrid(xs, ys)

    prediction_grid = np.zeros(xx.shape, dtype = int)
    for i,x in enumerate(xs):
        for j,y in enumerate(ys):
            p = np.array([x, y])
            prediction_grid[j,i] = knn_predict(p, predictors, outcomes, k)

    return (xx, yy, prediction_grid)
seasons = ["spring","summer","fall","winter"]
list(enumerate(seasons))
(predictors, outcomes) = genereate_synth_data()

from sklearn import datasets
iris = datasets.load_iris()
predictors = iris.data[:,0:2]
outcomes = iris.target
plt.plot(predictors[outcomes==0][:,0], predictors[outcomes==0][:,1], "ro")
plt.plot(predictors[outcomes==1][:,0], predictors[outcomes==1][:,1], "go")
plt.plot(predictors[outcomes==2][:,0], predictors[outcomes==2][:,1], "ro")
plt.savefig("iris.pdf")
k=5; filename="iris_gris.pdf"; limits = (4,8,1.5,4.5); h = 0.1
(xx, yy, prediction_grid) = make_prediction_grid(predictors, outcomes, limits, h, k)
plot_prediction_grid(xx,yy, prediction_grid, filename)

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(predictors, outcomes)
sk_predictions = knn.predict(predictors)
sk_predictions.shape
sk_predictions[0:10]
my_predictions = np.array([knn_predict(p, predictors, outcomes, 5) for p in predictors])