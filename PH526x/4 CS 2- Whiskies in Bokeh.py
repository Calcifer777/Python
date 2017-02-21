
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster.bicluster import SpectralCoclustering
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, output_file, show


############################################
###	Define whisky cluster groups via SCC method

# Import and merge the whiskies and regions txt files
whisky = pd.read_csv("whiskies.txt")
regions = pd.read_csv("regions.txt")
whisky["regions"] = regions

# Selects all columns between Body and Floral included
flavors = whisky.iloc[:, 2:14]

# Find clusters of whisky using the spectral coclustering technique
correlations = pd.DataFrame.corr(flavors.transpose())
model = SpectralCoclustering(n_clusters = 6, random_state = 0)
model.fit(correlations)
correlations = np.array(correlations)

# Extracts the group labels from the model and appends them to the whiskies table, specifying the index explicitly
whisky["Group"] = pd.Series(model.row_labels_, index = whisky.index)

# Order the rows by increasing order by using group labels, which have been discovered via the SCC method
whisky = whisky.ix[np.argsort(model.row_labels_)]

# Reset the index of the dataframe whiskies
whisky = whisky.reset_index(drop = True)

########################################################
# Use of the bokeh library

# Define a dictionary of regions and associated colors
cluster_colors = ["red", "orange", "green", "blue", "purple", "gray"]
regions = ["Speyside", "Highlands", "Lowlands", "Islands", "Campbelltown", "Islay"]
region_colors = dict(zip(regions, cluster_colors))

# Create a correlation color matrix. Assigns white to low correlation scores; assigns the color in cluste_colors to high correlation scores.
distilleries = list(whisky.Distillery)
correlation_colors = [ ]

for i in range(len(distilleries)):
	for j in range(len(distilleries)):
		if correlations[i,j] < .70:						# if low correlation,
			correlation_colors.append('white')			# just use white.
		else:                                          	# otherwise,
			if whisky.Group[i] == whisky.Group[j]:        # if the groups match,
				correlation_colors.append(cluster_colors[whisky.Group[i]]) # color them by their mutual group.
			else:                                      # otherwise
				correlation_colors.append('lightgray') # color them lightgray.

# print(correlation_colors)

###########################################
### PRINTING THE CORRELATION MATRIX
###########################################
source = ColumnDataSource(
    data = {
        "x": np.repeat(distilleries,len(distilleries)),
        "y": list(distilleries)*len(distilleries),
        "colors": correlation_colors,
        "alphas": correlations.flatten(),
        "correlations": correlations.flatten(),
    }
)

output_file("Whisky Correlations.html", title="Whisky Correlations")
fig = figure(title="Whisky Correlations",
    x_axis_location="above", tools="resize,hover,save",
    x_range=list(reversed(distilleries)), y_range=distilleries)
fig.grid.grid_line_color = None
fig.axis.axis_line_color = None
fig.axis.major_tick_line_color = None
fig.axis.major_label_text_font_size = "5pt"
fig.xaxis.major_label_orientation = np.pi / 3

fig.rect('x', 'y', .9, .9, source=source,
     color='colors', alpha='alphas')
hover = fig.select(dict(type=HoverTool))
hover.tooltips = {
    "Whiskies": "@x, @y",
    "Correlation": "@correlations",
}
show(fig)

