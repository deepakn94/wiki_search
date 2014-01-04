import wikipedia
import indexer
from collections import defaultdict

seeds = ['Djokovic']

pages = set()
visited_pages = set()

NUMBER_PAGES = 100000
NUMBER_PER_PAGE = 100


def get_page_content(page_name):
    page = wikipedia.page(page_name)
    global pages
    for link in page.links:
        if link not in pages and link not in visited_pages:
            pages.add(link)
    return page.content


if __name__ == '__main__':
    wikipedia.set_rate_limiting(True)
    for seed in seeds:
        pages.add(seed)
    reverse_index = defaultdict(list)
    i = 0
    while pages and i < NUMBER_PAGES:
        page_name = pages.pop()
        visited_pages.add(page_name)
        page_content = get_page_content(page_name)
        text = indexer.parse_document(page_content)
        index = indexer.construct_reverse_index(text, page_name)
        reverse_index = indexer.merge_reverse_indices(reverse_index, index)
        print "Just visited page %s (%dth page)..." % (page_name, (i + 1))
        i += 1
        if (i % NUMBER_PER_PAGE == 0):
            indexer.dump_index(reverse_index, ('index_%d.txt' % i))
