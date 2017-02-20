
import scipy.stats as ss
import numpy as np
import matplotlib.pyplot as plt

def generateSyntData(n = 50):
	points = np.concatenate((ss.norm(0,1).rvs((n,2)), ss.norm(1,1).rvs((n,2))), axis = 0)
	outcomes = np.concatenate((np.repeat(0, n), np.repeat(1, n)))
	return (points, outcomes)

n = 50
(points, outcomes) = generateSyntData(n)

plt.figure()
plt.plot(points[:n, 0], points[:n, 1], "bo")
plt.plot(points[n:, 0], points[n:, 1], "go")
plt.show()