from helpers import get_links
from graph import DiGraph

import os

# from pprint import pprint

filename = "graph.txt"

graph = DiGraph()

if os.path.isfile(filename):
    graph.read_from_filename(filename)

if graph.nodes:
    to_traverse = graph.get_to_traverse()
else:
    root_pagename = "Kevin_Bacon"
    to_traverse = {root_pagename}
count = len(graph.nodes)

# traverse whole graph
with open(filename, "a+", encoding="utf-8") as file:
    while to_traverse:
        pagename = to_traverse.pop()
        graph.add_node(pagename)
        count += 1

        print(f"Traversing {pagename}")
        print(count)

        for link in get_links(pagename):
            graph.add_link(pagename, link)
            if link in graph.nodes: continue
            to_traverse.add(link)    # BFS

        graph.write_node_to_file(file, pagename)
