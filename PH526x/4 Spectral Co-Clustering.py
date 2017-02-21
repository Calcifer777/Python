
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import and merge the whiskies and regions txt files
whiskies = pd.read_csv("whiskies.txt")
regions = pd.read_csv("regions.txt")
whiskies["regions"] = regions

# Selects all columns between Body and Floral included
flavors = whiskies.iloc[:, 2:14]

# Computes the correlation betweent the whiskies' attributes
corrFlavors = pd.DataFrame.corr(flavors)
fig, ax = plt.subplots()
plt.pcolor(corrFlavors, label = np.array(flavors.columns))	# Plots a heatmap of the matrix

plt.xticks(np.arange(0.5,len(flavors.columns)), list(corrFlavors.columns), rotation = 30)
plt.yticks(np.arange(0.5, len(flavors.columns)), list(corrFlavors.columns))
# ax.set_xticklabels(list(corrFlavors.columns))
# ax.set_yticklabels(list(corrFlavors.columns))
plt.colorbar()
plt.savefig("4 Correlations Heatmap.png")


# Computes the correlation between distilleries. Each column of the flavors table indicates a whisky produced by a given sistillery
corrWhisky = pd.DataFrame.corr(flavors.transpose())
fig, ax = plt.subplots()
plt.pcolor(corrWhisky, label = np.array(flavors.columns))	# Plots a heatmap of the matrix
plt.colorbar()
plt.savefig("4 Correlations Heatmap 2.png")

#########################################
#########################################

# Find correlation clusters of whiskies using the spectral coclustering technique

from sklearn.cluster.bicluster import SpectralCoclustering

model = SpectralCoclustering(n_clusters = 6, random_state = 0)

model.fit(corrWhisky)

# Prints how the whiskies have been classified into clusters
clusters = np.sum(model.rows_, axis = 1)
print(clusters)

# Prints to which cluster each whisky belongs
whiskiesClassified = model.row_labels_
print(whiskiesClassified)
#####################################
# Comparing correlation matrices

# Extracts the group labels from the model and appends them to the whiskies table, specifying the index explicitly
whiskies["Group"] = pd.Series(model.row_labels_, index = whiskies.index)

# Order the rows by increasing order by using group labels, which have been discovered via the SCC method
whiskies = whiskies.ix[np.argsort(model.row_labels_)]

# Reset the index of the dataframe whiskies
whiskies = whiskies.reset_index(drop = True)

# Recalculate the correlation matrix and turn it to a np.array object
correlations = pd.DataFrame.corr(whiskies.iloc[:, 2:14].transpose())

correlations = np.array(correlations)

# Plots the new correlation matrix
plt.figure()
plt.subplot(121)
plt.pcolor(corrWhisky)
plt.title("Original")
plt.subplot(122)
plt.pcolor(correlations)
plt.title("Rearranged")
plt.colorbar()
plt.savefig("4 Correlation Clustering.png")

# !!! The spectral coclustering methods allows to find groups of objects that are similar according to a series of characteristics. In this case, the whiskies belonging to each of the 6 clusters should be similar in flavor, that is, according to the characteristics/columns in the input table.