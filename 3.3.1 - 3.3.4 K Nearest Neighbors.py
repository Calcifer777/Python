import random
import scipy.stats as ss
import numpy as np
import matplotlib.pyplot as plt

def mode(vector):

	dictFrequencies = {}
	for i in vector:
		if i in dictFrequencies:
			dictFrequencies[i] += 1
		else:
			dictFrequencies[i] = 1
	lsMode = []
	intMaxCount = max(dictFrequencies.values())
	for key, value in dictFrequencies.items():
		if value == intMaxCount:
			lsMode.append(key)
	return random.choice(lsMode)

def distance(p1, p2, power = 2):
	return np.sqrt(sum(np.power(p1-p2, power)))

data = np.array([[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]])

outcomes = np.array(["OK","OK","OK","OK","KO","KO","KO","KO","KO"])

p = np.array([1,2.3])

def knn(p, data, k=3):
	distances = np.zeros(data.shape[0])
	for i in range(len(data)):
		distances[i] = distance(p, data[i])
	ind = np.argsort(distances)
	return ind[:k]

def knnPredict(p, data, outcomes, threshold):
	ind = knn(p, data, threshold)
	return mode(outcomes[ind])

result = knnPredict(p, data, outcomes, 2)
print(result)
knn = data[knn(p, data)]

plt.plot(data[:,0], data[:,1], "bo")
plt.plot(p[0], p[1], "ro")
plt.plot(knn[:,0], knn[:,1], "gD")

print(data.shape)