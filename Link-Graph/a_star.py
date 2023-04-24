from collections import defaultdict, deque
from queue import Queue
import numpy as np
import heapq
import signal
import timeit
from functools import partial

def reconstruct_path(start, goal, backlinks, id_titles):
    path = []
    curr = goal

    while curr != start:
        path.insert(0, curr)
        curr = backlinks[curr]

    path.insert(0, start)
    return [id_titles[x] for x in path]

def signal_handler(signum, frame):
    raise Exception

class A_Star(object):
    def __init__(self, graph, title_ids, id_titles):
        self.graph = graph
        self.expanded_nodes = 0
        self.title_ids = title_ids
        self.id_titles = id_titles
    
    def dummy_heuristic(self,start, goal, curr):
        return 0
    
    def get_shortest_path(self, start, goal, heuristic, disallow=[], print_progress=True, time_limit=10):
        if heuristic == "dummy":
            return self.shortest_path_heuristic(start, goal, self.dummy_heuristic, disallow, print_progress,time_limit)
        else:
            print("invalid heuristic")
    
    def shortest_path_heuristic(self, start, goal, heuristic, disallow, print_progress, time_limit):
        self.expanded_nodes = 0
        start_id, goal_id = self.title_ids[start], self.title_ids[goal]
        #use signal to manage time limit
        handler = signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(time_limit)
        start_time = timeit.default_timer()
        
        try:
            g_score = defaultdict(lambda: 999999)
            f_score = defaultdict(lambda: 999999)

            g_score[start_id] = 0
            f_score[start_id] = 0

            open_set = []
            open_set_mirror = set()     # mirror of open_set with O(1) lookup

            heapq.heappush(open_set, (f_score[start_id], start_id))   # (f_score, id)
            open_set_mirror.add(start_id)

            backlinks = {}

            while open_set:
                self.expanded_nodes += 1
                _, curr = heapq.heappop(open_set)
                open_set_mirror.remove(curr)

                if curr == goal_id:
                    path_titles = reconstruct_path(start_id, goal_id, backlinks, self.id_titles)
                    elapsed_time = timeit.default_timer() - start_time
                    return path_titles, elapsed_time, self.expanded_nodes
                
                for link in self.graph[curr]:
                    tentative_g_score = g_score[curr] + 1
                    if tentative_g_score < g_score[link]:
                        backlinks[link] = curr
                        g_score[link] = tentative_g_score
                        f_score[link] = tentative_g_score + heuristic(start_id, goal_id, link)
                        if link not in open_set_mirror:
                            heapq.heappush(open_set, (f_score[link], link))
                            open_set_mirror.add(link)
        except Exception:
            return None, time_limit, self.expanded_nodes
        finally:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(0)

