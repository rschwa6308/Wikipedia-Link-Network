from GraphRendering.Render import run_system
from GraphRendering.Graphs import Graph
from GraphRendering.Physics import System



from graph import DiGraph
import os
import random

filename = "graph.txt"

graph = DiGraph()

if os.path.isfile(filename):
    graph.read_from_filename(filename)

print("Loading Complete.")



# start, end = random.sample(list(graph.nodes), 2)
start = "Kevin_Bacon"
end = "Computer_language"

assert(end in graph.nodes)

nodes = graph.shortest_path(start, end)

# for n in list(nodes):
#     nodes.extend(
#         random.sample([c for c in graph.nodes[n] if c in graph.nodes], 3)
#     )

nodes = set(nodes)      # make unique


test_graph = Graph(
    list(nodes),
    [
        (a, b, 1) for a in nodes for b in nodes
        if b in graph.nodes[a] and a != b
    ]
)

test_system = System.from_graph(
    test_graph
)

print(start, end)

run_system(test_system)

