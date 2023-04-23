from collections import defaultdict, deque
from queue import Queue
import numpy as np
import heapq
import signal
import timeit
from functools import partial

def signal_handler(signum, frame):
    raise Exception

def reconstruct_path(start, goal, backlinks, id_titles):
    path = []
    curr = goal

    while curr != start:
        path.insert(0, curr)
        curr = backlinks[curr]

    path.insert(0, start)
    return [id_titles[x] for x in path]

class BFS_Search(object):
    def __init__(self, graph, title_ids, id_titles):
        self.graph = graph
        self.queue = Queue()
        self.expanded_nodes = 0
        self.title_ids = title_ids
        self.id_titles = id_titles

    def shortest_path(self,start, goal, disallow=[], print_progress=False, time_limit=10):
        self.expanded_nodes = 0
        #get IDs for start and end node
        start_id, goal_id = self.title_ids[start], self.title_ids[goal]
        #use signal to manage time limit
        handler = signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(time_limit)
        start_time = timeit.default_timer()
        #start search
        try:
            self.queue.put(start_id)

            backlinks = {}

            while not self.queue.empty():
                curr = self.queue.get()
                self.expanded_nodes += 1

                for link in self.graph[curr]:
                    if link in backlinks:
                        continue
                        
                    backlinks[link] = curr

                    if link in disallow:
                        continue
                    
                    if link == goal_id:
                        path = reconstruct_path(start_id, goal_id, backlinks, self.id_titles)
                        elapsed_time = timeit.default_timer() - start_time
                        return path, round(elapsed_time,2), self.expanded_nodes
                
                    self.queue.put(link)

                    if print_progress:
                        # if len(extended_path) - 1 > depth:
                        #     depth = len(extended_path) - 1
                        #     print(f"Searching depth {depth} ...")
                        #     print("\tSearched:", len(backlinks))
                        if len(backlinks) % 500_000 == 0:
                            print("\tSearched:", len(backlinks))
        except Exception:
            return None, time_limit, self.expanded_nodes
        finally:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(0)