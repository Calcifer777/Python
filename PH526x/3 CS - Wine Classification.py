import pandas as pd
import sklearn.decomposition
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.neighbors import KNeighborsClassifier

def accuracy(predictions, outcomes):
   """ Returns the percentage of equal elements between two vectors"""
   return sum(predictions == outcomes)/len(predictions)

data = pd.read_csv(r'https://s3.amazonaws.com/demo-datasets/wine.csv')

# !!! The r before the url string escapes the special characters in the whole string

numericData =  data.drop("color", axis = 1)
numericData -= numericData.mean()
numericData /= numericData.std()

pca = sklearn.decomposition.PCA(n_components=2)

principal_components = pca.fit(numericData).transform(numericData)

observation_colormap = ListedColormap(['red', 'blue'])
x = principal_components[:,0] 
y = principal_components[:,1]

plt.title("Principal Components of Wine")
plt.scatter(x, y, alpha = 0.2,
    c = numericData['high_quality'], cmap = observation_colormap, edgecolors = 'none')
plt.xlim(-8, 8); plt.ylim(-8, 8)
plt.xlabel("Principal Component 1"); plt.ylabel("Principal Component 2")
plt.savefig("3 CS - Principal Components Plot")
plt.show()

knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(numericData, data['high_quality'])

library_predictions = knn.predict(numericData)

print(accuracy(library_predictions, data["high_quality"]))


