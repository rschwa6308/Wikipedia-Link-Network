import bz2
import re

from article_titles import ARTICLE_TITLES



def parse_tags_from_xml(xml, tag):
    pattern = fr"\<{tag}\>(.+)\<\/{tag}\>"
    return re.findall(pattern, xml)


def parse_links_from_xml(xml):
    matches = re.findall(r"\[\[([^\]]+)\]\]", xml)
    link_texts = [m.partition("|")[0] for m in matches]
    return [lt for lt in link_texts if lt]


def link_text_to_article_title(link_text):
    "E.g.: 'public transit' -> 'Public_transit'"
    no_spaces = link_text.replace(" ", "_")
    if len(no_spaces) > 1:
        return no_spaces[0].upper() + no_spaces[1:]
    else:
        return no_spaces[0].upper()



def iter_page_xmls(filename):
    assert filename.endswith(".bz2")
    page = ""
    in_page = False
    with bz2.open(filename, mode="rt", encoding="UTF-8") as f:
        for line in f.readlines():
            if line.strip() == "<page>":
                in_page = True

            if in_page:
                page += line
            
            if line.strip() == "</page>":
                yield page
                page = ""
                in_page = False


# TODO
# - filter for article links
# - filter out redirects




if __name__ == "__main__":
    for page in iter_page_xmls("Wikipedia-Dumps/test/enwiki-20221220-pages-articles-multistream1.xml-p1p41242.bz2"):
        # print(page)
        title = parse_tags_from_xml(page, "title")[0]
        title = link_text_to_article_title(title)

        if title not in ARTICLE_TITLES:
            print("WEIRD!!!", title)
        # assert title in ARTICLE_TITLES

        links = parse_links_from_xml(page)
        links = map(link_text_to_article_title, links)
        links = [l for l in links if l in ARTICLE_TITLES]
        print(f"{title}: {', '.join(links[:10])}")
        print()

        # break
