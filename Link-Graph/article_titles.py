import gzip

ARTICLE_TITLES = set()

with gzip.open("Wikipedia-Dumps/20221220/enwiki-20221220-all-titles-in-ns0.gz", "rt") as f:
    for line in f.readlines():
        title = line.strip()
        ARTICLE_TITLES.add(title)

print(len(ARTICLE_TITLES))
