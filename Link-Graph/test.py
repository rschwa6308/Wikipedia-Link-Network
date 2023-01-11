from tqdm import tqdm

TITLES_TO_IDS = {}
IDS_TO_TILES = {}

with open("Link-Graph/ID_map.txt") as f:
    for line in tqdm(f.readlines()):
        title, ID = line.split()
        ID = int(ID)

        TITLES_TO_IDS[title] = ID
        IDS_TO_TILES[ID] = title


from random import randint

random_ID = randint(0, 16_000_000)
title = IDS_TO_TILES[random_ID]
print(title)