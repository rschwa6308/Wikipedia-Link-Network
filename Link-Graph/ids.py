from collections import defaultdict, deque
from queue import Queue
import numpy as np
import timeit
import signal
import heapq
from functools import partial

def signal_handler(signum, frame):
    raise Exception

class ID_Search(object):
    def __init__(self, graph, title_ids, id_titles):
        self.graph = graph
        self.title_ids = title_ids
        self.id_titles = id_titles
    
    def reconstruct_path(self, path, id_titles):
        return [id_titles[x] for x in path]

    def depth_limited_search(self, curr, goal, depth_limit):
        self.expanded_nodes += 1
        # explored[curr] = depth_limit

        # print(IDS_TO_TILES[curr], depth_limit)

        if depth_limit == 0:
            if curr == goal:
                return ((curr,), True)
            else:
                return (None, True)
        
        any_remaining = False
        for link in self.graph[curr]:
            # if link in explored and depth_limit-1 < explored[link]:
            #     print("savings!")
            #     continue

            # print(f"\t{IDS_TO_TILES[curr]} -> {IDS_TO_TILES[link]}")

            # backlinks[link] = curr

            path, remaining = self.depth_limited_search(link, goal, depth_limit-1)

            if path is not None:
                return ((curr,)+path, True)
            
            if remaining:
                any_remaining = True
        
        return (None, any_remaining)

    def shortest_path(self,start, goal, disallow=[], print_progress=False, time_limit=10):
        self.expanded_nodes = 0
        #get IDs for start and end node
        start_id, goal_id = self.title_ids[start], self.title_ids[goal]
        #use signal to manage time limit
        handler = signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(time_limit)
        start_time = timeit.default_timer()
        #start search
        depth_limit = 1
        try:
            while True:
                if print_progress:
                    print(f"Searching depth {depth_limit} ...")

                path, remaining = self.depth_limited_search(start_id, goal_id, depth_limit)

                if path is not None:
                    title_path = self.reconstruct_path(path, self.id_titles)
                    elapsed_time = timeit.default_timer() - start_time
                    return title_path, elapsed_time, self.expanded_nodes
                
                if not remaining:
                    return None     # no path found

                depth_limit += 1
        except Exception as e:
            print(e)
            return None, time_limit, self.expanded_nodes
        finally:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(0)