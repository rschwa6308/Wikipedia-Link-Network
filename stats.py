from graph import DiGraph
import os
from matplotlib import pyplot as plt
import scipy.stats
import numpy as np

filename = "graph.txt"

graph = DiGraph()

if os.path.isfile(filename):
    graph.read_from_filename(filename)

print("Loading Complete.")

num_links = []
for links in graph.nodes.values():
    num_links.append(len(links))


print(scipy.stats.describe(num_links))
print(f"Avg. Length : {np.mean(list(map(len, graph.nodes)))}")

plt.hist(num_links, bins=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200])
plt.show()


print(max(graph.nodes, key=lambda n: len(graph.nodes[n])))
