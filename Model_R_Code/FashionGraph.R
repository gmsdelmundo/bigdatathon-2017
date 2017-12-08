setwd("/Users/BlackHawk/Desktop/")
theBigDeeData = read.csv("Imputed.csv", header = TRUE, stringsAsFactors = FALSE)
rownames(theBigDeeData) <- theBigDeeData[,1]
theBigDeeData = theBigDeeData[,2:ncol(theBigDeeData)]
# Now we have the data formated the way we want!

library(GGMselect) 
# You can read the package details here:
# https://cran.r-project.org/web/packages/GGMselect/vignettes/Notice.pdf
# Notice on pg. 4, "The Lasso-And family GbLA derives from the estimation procedure proposed by 
# Meinshausen and Bühlmann". That's exactly what we want!
# One line of code...
graph_computation = selectFast(as.matrix(theBigDeeData), K=2, family = "LA")

# G is a matrix of the graph in graph_computation
# We need to create a graph from the matrix, and can treat matrix like adjecency mat
library(igraph)
graph_to_plot = graph_from_adjacency_matrix(graph_computation$LA$G, mode = "undirected")

#name the vertecies, V(graph) will return all the vertecies for graph
temp = seq(1,length(names_of_rows))
name_dictionary = data.frame(temp, names_of_rows)
V(graph_to_plot)$name <- temp
plot.igraph(graph_to_plot)
View(name_dictionary)