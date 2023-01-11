from graph import DiGraph
import os
import random


filename = "graph.txt"

graph = DiGraph()

if os.path.isfile(filename):
    graph.read_from_filename(filename)

print("Loading Complete.")



with open("temp.txt", "w+", encoding="utf-8") as f:
    f.write("\n".join(graph.nodes))