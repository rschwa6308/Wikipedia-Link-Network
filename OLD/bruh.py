from graph import DiGraph
import os
import random

filename = "graph.txt"

graph = DiGraph()

if os.path.isfile(filename):
    graph.read_from_filename(filename)

print("Loading Complete.")
node1 = random.choice(list(graph.nodes))
node2 = random.choice(list(graph.nodes))

print(graph.shortest_path(node1, node2))