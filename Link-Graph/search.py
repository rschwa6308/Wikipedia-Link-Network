from queue import Queue
import numpy as np


# module-level globals (to be filled in by caller)
GRAPH = None
TITLES_TO_IDS, IDS_TO_TILES = None, None


def shortest_path_id(start, goal, disallow=[], print_progress=True):
    "BFS from start page ID to goal page ID"
    queue = Queue()
    queued = set()      # keep track of pages already put into the queue

    queue.put((start,))
    queued.add(start)

    depth = 0
    
    while not queue.empty():
        curr = queue.get()

        for link in GRAPH[curr[-1]]:
            if link in queued:
                continue
            
            if link in disallow:
                continue

            extended_path = curr + (link,)

            if link == goal:
                return extended_path

            queue.put(extended_path)
            queued.add(link)

            if print_progress:
                if len(extended_path) - 1 > depth:
                    depth = len(extended_path) - 1
                    print(f"Searching depth {depth} ...")
                    print("\tSearched:", len(queued))
                if len(queued) % 500_000 == 0:
                    print("\tSearched:", len(queued))


def shortest_path(start, goal, disallow=[], print_progress=True):
    start_ID, goal_ID = TITLES_TO_IDS[start], TITLES_TO_IDS[goal]
    disallow_IDs = [TITLES_TO_IDS[x] for x in disallow]

    path_IDs = shortest_path_id(start_ID, goal_ID, disallow=disallow_IDs, print_progress=print_progress)

    if path_IDs is None:
        return None

    return [IDS_TO_TILES[x] for x in path_IDs]

