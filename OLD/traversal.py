from helpers import get_links
from graph import DiGraph

from pprint import pprint

root_pagename = "NBC"

graph = DiGraph()



# visited = set()
to_traverse = [root_pagename]

# traverse whole graph
while to_traverse:
    pagename = to_traverse.pop(0)
    graph.add_node(pagename)

    # visited.add(pagename)
    print(f"Traversing {pagename}")
    for link in get_links(pagename):
        graph.add_link(pagename, link)
        if link in graph.nodes: continue
        to_traverse.append(link)    # BFS

    # print("\n".join(to_traverse))
    # break
    if len(graph.nodes) >= 100:
        # pprint(graph.nodes)
        break


graph.write_to_file("graph.txt")
