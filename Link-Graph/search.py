from collections import defaultdict, deque
from queue import Queue
import numpy as np
import heapq
from functools import partial


# module-level globals (to be filled in by caller)
GRAPH, TRANSPOSE_GRAPH = None, None
TITLES_TO_IDS, IDS_TO_TILES = None, None




def reconstruct_path(start, goal, backlinks):
    path = []
    curr = goal

    while curr != start:
        path.insert(0, curr)
        curr = backlinks[curr]

    path.insert(0, start)

    return path



def shortest_path_BFS_id(start, goal, disallow=[], print_progress=True):
    "BFS from start page ID to goal page ID"
    queue = Queue()
    queue.put(start)

    backlinks = {}
    
    while not queue.empty():
        curr = queue.get()

        for link in GRAPH[curr]:
            if link in backlinks:
                continue

            backlinks[link] = curr
            
            if link in disallow:
                continue

            if link == goal:
                return reconstruct_path(start, goal, backlinks)

            queue.put(link)

            if print_progress:
                # if len(extended_path) - 1 > depth:
                #     depth = len(extended_path) - 1
                #     print(f"Searching depth {depth} ...")
                #     print("\tSearched:", len(backlinks))
                if len(backlinks) % 500_000 == 0:
                    print("\tSearched:", len(backlinks))
                


def shortest_path_IDS_id(start, goal, disallow=[], print_progress=True):
    "Iterative Deepening Search from start page ID to goal page ID"

    # explored = {}

    def depth_limited_search(curr, depth_limit):
        # explored[curr] = depth_limit

        # print(IDS_TO_TILES[curr], depth_limit)

        if depth_limit == 0:
            if curr == goal:
                return ((curr,), True)
            else:
                return (None, True)
        
        any_remaining = False
        for link in GRAPH[curr]:
            # if link in explored and depth_limit-1 < explored[link]:
            #     print("savings!")
            #     continue

            # print(f"\t{IDS_TO_TILES[curr]} -> {IDS_TO_TILES[link]}")

            # backlinks[link] = curr

            path, remaining = depth_limited_search(link, depth_limit-1)

            if path is not None:
                return ((curr,)+path, True)
            
            if remaining:
                any_remaining = True
        
        return (None, any_remaining)
        

    depth_limit = 1
    while True:
        if print_progress:
            print(f"Searching depth {depth_limit} ...")
        
        # backlinks.clear()
        # explored.clear()
        path, remaining = depth_limited_search(start, depth_limit)

        # if found is not None:
        #     return reconstruct_path(start, goal, backlinks)

        if path is not None:
            return path
        
        if not remaining:
            return None     # no path found

        depth_limit += 1



def shortest_path_ASTAR_id(start, goal, heuristic, disallow=[], print_progress=True):
    "A* Search from start page ID to goal page ID"

    g_score = defaultdict(lambda: 999999)
    f_score = defaultdict(lambda: 999999)

    g_score[start] = 0
    f_score[start] = 0

    open_set = []
    open_set_mirror = set()     # mirror of open_set with O(1) lookup

    heapq.heappush(open_set, (f_score[start], start))   # (f_score, id)
    open_set_mirror.add(start)


    backlinks = {}

    while open_set:
        _, curr = heapq.heappop(open_set)
        open_set_mirror.remove(curr)

        # print(IDS_TO_TILES[curr])

        if curr == goal:
            return reconstruct_path(start, goal, backlinks)
        
        for link in GRAPH[curr]:
            tentative_g_score = g_score[curr] + 1
            if tentative_g_score < g_score[link]:
                backlinks[link] = curr
                g_score[link] = tentative_g_score
                f_score[link] = tentative_g_score + heuristic(start, goal, link)
                if link not in open_set_mirror:
                    heapq.heappush(open_set, (f_score[link], link))
                    open_set_mirror.add(link)



def dummy_heuristic(start, goal, curr):
    return 0



# Landmarks Heuristic:
# https://www.cs.princeton.edu/courses/archive/spr06/cos423/Handouts/GH05.pdf


TO_LANDMARK_DISTANCES = {}
FROM_LANDMARK_DISTANCES = {}

def compute_landmark_distances(landmarks):

    for landmark in landmarks:
        print(f"Computing distances from landmark: {IDS_TO_TILES[landmark]}")
        max_dist = -1

        distances = {}
        distances[landmark] = 0

        # BFS from the landmark outwards in the original graph
        queue = Queue()
        queue.put(landmark)
        
        while not queue.empty():
            curr = queue.get()

            if distances[curr] > max_dist:
                max_dist = distances[curr]
                print(f"depth: {max_dist} ({IDS_TO_TILES[curr]})")
            
            # print(IDS_TO_TILES[curr], GRAPH[curr])

            for link in GRAPH[curr]:
                # print(link)
                if link in distances:
                    continue

                distances[link] = distances[curr] + 1

                queue.put(link)

                if len(distances) % 1_000_000 == 0:
                    print(len(distances))
        
        FROM_LANDMARK_DISTANCES[landmark] = distances


        print(f"Computing distances to landmark: {IDS_TO_TILES[landmark]}")
        max_dist = -1

        distances = {}
        distances[landmark] = 0

        # BFS from the landmark outwards in the transpose graph
        queue = Queue()
        queue.put(landmark)
        
        while not queue.empty():
            curr = queue.get()

            if distances[curr] > max_dist:
                max_dist = distances[curr]
                print(f"depth: {max_dist} ({IDS_TO_TILES[curr]})")

            for link in TRANSPOSE_GRAPH[curr]:
                if link in distances:
                    continue

                distances[link] = distances[curr] + 1

                queue.put(link)

                if len(distances) % 1_000_000 == 0:
                    print(len(distances))
        
        TO_LANDMARK_DISTANCES[landmark] = distances



def dist_to_landmark(curr, landmark):
    "look up the precomputed exact distance from curr to landmark"
    return TO_LANDMARK_DISTANCES[landmark].get(curr, 9999999)


def dist_from_landmark(curr, landmark):
    "look up the precomputed exact distance from landmark to curr"
    return FROM_LANDMARK_DISTANCES[landmark].get(curr, 9999999)


def landmarks_heuristic(start, goal, curr):
    vals = []

    for landmark in TO_LANDMARK_DISTANCES:
        vals.append(dist_to_landmark(curr, landmark) - dist_to_landmark(goal, landmark))
    
    for landmark in FROM_LANDMARK_DISTANCES:
        vals.append(dist_from_landmark(goal, landmark) - dist_to_landmark(curr, landmark))

    return max(vals)



def shortest_path(start, goal, disallow=[], print_progress=True, method="BFS"):
    start_ID, goal_ID = TITLES_TO_IDS[start], TITLES_TO_IDS[goal]
    disallow_IDs = [TITLES_TO_IDS[x] for x in disallow]

    method_map = {
        "BFS": shortest_path_BFS_id,
        "IDS": shortest_path_IDS_id,
        "A* dummy": partial(shortest_path_ASTAR_id, heuristic=dummy_heuristic),
        "A* landmarks": partial(shortest_path_ASTAR_id, heuristic=landmarks_heuristic),
    }

    if method not in method_map:
        raise ValueError("Invalid method name")
    
    searcher = method_map[method]

    path_IDs = searcher(start_ID, goal_ID, disallow=disallow_IDs, print_progress=print_progress)
    
    if path_IDs is None:
        return None

    return [IDS_TO_TILES[x] for x in path_IDs]

