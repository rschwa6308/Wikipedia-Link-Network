from tqdm import tqdm
import numpy as np
# from scipy.sparse import dok_array, csr_array, lil_array


def read_ID_map(filename):
    TITLES_TO_IDS = {}
    IDS_TO_TILES = {}

    with open(filename) as f:
        for line in tqdm(f.readlines(), desc="Reading ID Map"):
            title, ID = line.split()
            ID = np.uint32(int(ID))

            TITLES_TO_IDS[title] = ID
            IDS_TO_TILES[ID] = title
    
    return TITLES_TO_IDS, IDS_TO_TILES



def read_link_graph(filename):
    GRAPH = {}

    with open(filename) as f:
        for line in tqdm(f.readlines(), desc="Reading Graph"):
            title_ID, _, link_IDs = line.partition(": ")
            title_ID = np.int32(int(title_ID))
            link_IDs = np.array([int(l) for l in link_IDs.strip().split()], dtype=np.int32)
            if title_ID in GRAPH:
                # print(f"WARNING: duplicate entry found for '{IDS_TO_TILES[title_ID]}' ({title_ID}). Skipping...")
                continue
            GRAPH[title_ID] = link_IDs

    return GRAPH