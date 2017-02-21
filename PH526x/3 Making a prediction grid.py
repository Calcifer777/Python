
import scipy.stats as ss
import numpy as np
import matplotlib.pyplot as plt
import random

def generateSyntData(n = 50):
	points = np.concatenate((ss.norm(0,1).rvs((n,2)), ss.norm(1,1).rvs((n,2))), axis = 0)
	outcomes = np.concatenate((np.repeat(0, n), np.repeat(1, n)))
	return (points, outcomes)

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
	"""Returns the nth order distance between two points"""	
	return np.sqrt(sum(np.power(p1-p2, power)))

def knn(p, data, k=3):
	""" Given a point and a dataset, calculates the k nearest neighbors to that point"""	
	distances = np.zeros(data.shape[0])
	for i in range(len(data)):
		distances[i] = distance(p, data[i])
	ind = np.argsort(distances)
	return ind[:k]

def knnPredict(p, data, outcomes, threshold):
	""" Classifies the type of a vector observation via KNN"""
	ind = knn(p, data, threshold)
	return mode(outcomes[ind])

def makePredictionGrid(predictors, outcomes, limits, h, k):
	""" Classifies each point on the prediction grid via KNN."""
	(xMin, xMax, yMin, yMax) = limits
	xs = np.arange(xMin, xMax, h)
	ys = np.arange(yMin, yMax, h)
	xx, yy = np.meshgrid(xs, ys)

	predictionGrid = np.zeros(xx.shape, dtype = int)
	for i, x in enumerate(xs):
		for j, y in enumerate(ys):
			p = np.array([x, y])
			predictionGrid[j,i] = knnPredict(p, predictors, outcomes, k)
	return(xx, yy, predictionGrid)

def plotPredictionPrid (xx, yy, prediction_grid, filename):
    """ Plots KNN predictions for every point on the grid."""
    from matplotlib.colors import ListedColormap
    background_colormap = ListedColormap (["hotpink","lightskyblue", "yellowgreen"])
    observation_colormap = ListedColormap (["red","blue","green"])
    plt.figure(figsize =(10,10))
    plt.pcolormesh(xx, yy, prediction_grid, cmap = background_colormap, alpha = 0.5)
    plt.scatter(predictors[:,0], predictors [:,1], c = outcomes, cmap = observation_colormap, s = 50)
    plt.xlabel('Variable 1'); plt.ylabel('Variable 2')
    plt.xticks(()); plt.yticks(())
    plt.xlim (np.min(xx), np.max(xx))
    plt.ylim (np.min(yy), np.max(yy))
    plt.savefig(filename)

# Generating the data

(predictors, outcomes) = generateSyntData(n = 50)
k = 5
filename = "knnSynth.pdf"
limits = (-3, 4, -3, 4)
h = 0.1

(xx, yy, predictionGrid) = makePredictionGrid(predictors, outcomes, limits, h, k)

plotPredictionPrid(xx, yy, predictionGrid, filename)
