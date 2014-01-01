import urllib2
from bs4 import BeautifulSoup

seeds = ['/wiki/Djokovic']

# TODO: May need to use the Wikipedia API to extract text from
# the Wikipedia articles

urls = set()
visited_urls = set()


def get_page_content(url):
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    return html


def parse_html(html):
    soup = BeautifulSoup(html)
    href_tags = soup.find_all(href=True)
    hrefs = [href_tag.get('href') for href_tag in href_tags]
    global urls
    for href in hrefs:
        if '#' in href:
            continue
        if href.startswith('/wiki'):
            if href not in visited_urls and href not in urls:
                urls.add(href)


if __name__ == '__main__':
    global urls
    global visited_urls
    for seed in seeds:
        urls.add(seed)
    while urls:
        href = urls.pop()
        visited_urls.add(href)
        url = 'http://en.wikipedia.org%s' % href
        print 'Visiting %s now...' % url
        html = get_page_content(url)
        parse_html(html)
