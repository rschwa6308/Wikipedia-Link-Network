import os
from tqdm import tqdm

from parsing import *



dumps_dir = "Wikipedia-Dumps/20221220/articles"

output_filename = "Link-Graph/link_graph.txt"

with open(output_filename, "a+") as output_file:
    pages_processed = 0
    for dump_filename in tqdm(sorted(os.listdir(dumps_dir))):
        print(f"Processing {dump_filename} ...")
        for page in tqdm(iter_page_xmls(os.path.join(dumps_dir, dump_filename))):
            title = parse_tags_from_xml(page, "title")[0]
            title = link_text_to_article_title(title)

            if title not in ARTICLE_TITLES:
                continue

            links = parse_links_from_xml(page)
            links = map(link_text_to_article_title, links)
            links = [l for l in links if l in ARTICLE_TITLES]
            links = sorted(set(links))

            output_file.write(f"{title}: {', '.join(links)}\n")

            pages_processed += 1

        print()
        print(f"Pages Processed: {pages_processed}")
        print()
