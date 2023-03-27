import requests
from bs4 import BeautifulSoup


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
