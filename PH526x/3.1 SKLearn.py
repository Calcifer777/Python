from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

# Importing data from the iris dataset. This data is about flowers; it contains info about petal and sepal width and length. There are 3 types of flowers.

iris = datasets.load_iris()
predictors = iris.data[:, 0:2]
outcomes = iris.target

plt.plot(predictors[outcomes == 0] [:, 0], predictors[outcomes == 0] [:, 1], "ro")
plt.plot(predictors[outcomes == 1] [:, 0], predictors[outcomes == 1] [:, 1], "go")
plt.plot(predictors[outcomes == 2] [:, 0], predictors[outcomes == 2] [:, 1], "bo")
plt.show()

k = 5
limits = (4, 8, 1.5, 4,5)
h = 0.1
filename = "irisGrid.pdf"

knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(predictors, outcomes)
skPredictions = knn.predict(predictors)

# skPredictions contains the predictions about the classification of the iris flowers using the python inbuilt method.