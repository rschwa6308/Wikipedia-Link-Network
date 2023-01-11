from tqdm import tqdm


print("Building ID Map...")

TITLES_TO_IDS = {}
IDS_TO_TILES = {}

n = 0
with open("Link-Graph/link_graph.txt") as f:
    for line in tqdm(f.readlines()):
        title, _, _ = line.partition(":")
        if title not in TITLES_TO_IDS:
            TITLES_TO_IDS[title] = n
            IDS_TO_TILES[n] = title
            n += 1



print("Writing ID Map...")

with open("Link-Graph/ID_map.txt", "a+") as f:
    for title in tqdm(sorted(TITLES_TO_IDS.keys())):
        ID = TITLES_TO_IDS[title]
        f.write(f"{title} {ID}\n")



print("Writing Link Graph with IDs...")

with open("Link-Graph/link_graph_IDs.txt", "a+") as f_out:
    with open("Link-Graph/link_graph.txt", "r") as f_in:
        for line in tqdm(f_in.readlines()):
            title, _, links = line.partition(":")
            links = links.strip().split(", ")

            title_id = TITLES_TO_IDS[title]
            link_ids = [TITLES_TO_IDS.get(l, -1) for l in links if l]
            link_ids = [l for l in link_ids if l != -1]
            link_ids.sort()

            f_out.write(f"{title_id}: {' '.join(map(str, link_ids))}\n")

