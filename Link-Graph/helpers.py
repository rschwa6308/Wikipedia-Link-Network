import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import numpy as np


def build_transpose_graph(GRAPH):
    TRANSPOSE_GRAPH = {}

    for page in tqdm(GRAPH, desc="Initializing Transpose Graph"):
        TRANSPOSE_GRAPH[page] = np.array(dtype=np.uint32)

    for page in tqdm(GRAPH, desc="Building Transpose Graph"):
        for link in GRAPH[page]:
            TRANSPOSE_GRAPH[link].append(page)

    return TRANSPOSE_GRAPH
 



def fetch_page_html(page_title):
    url = f"https://en.wikipedia.org/wiki/{page_title}"
    r = requests.get(url)
    html = r.text
    return html


def find_link_text_in_html(html, target_page_title):
    soup = BeautifulSoup(html, "html.parser")

    target_page_url_relative = f"/wiki/{target_page_title}"
    target_link_tag = soup.find("a", href=target_page_url_relative)

    if target_link_tag is None:
        return None
    
    return target_link_tag.get_text().strip()




# TESTING
if __name__ == "__main__":
    html = fetch_page_html("Cliff_Thorburn")
    res = find_link_text_in_html(html, "Snooker")
    print(res)
