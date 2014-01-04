import wikipedia
import indexer

seeds = ['Djokovic']

pages = set()
visited_pages = set()


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
    while pages:
        page_name = pages.pop()
        visited_pages.add(page_name)
        page_content = get_page_content(page_name)
        text = indexer.parse_document(page_content)
        print text[:100]
        print "Just visited page %s..." % page_name
