# import module
import bs4
import re
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get(url):
    
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        result = session.get(url, verify=False)
    except requests.ConnectionError: 
        print("timed out - " + url)
    
    return result

def crawl_single_page(url, regex):
    request_result = get(url)

    if request_result == None:
        return False, []

    global total_pages_crawled
    total_pages_crawled += 1
    print("crawled page~! - " + str(total_pages_crawled))
    print(url)

    html = request_result.text

    soup = bs4.BeautifulSoup(html, "html.parser")

    is_hit = re.search(regex, html)

    urls = []

    for a in soup.find_all('a', href=True):
        href = a['href']
        url = requests.compat.urljoin(url, href)

        urls.append(url)

    return is_hit, urls

def should_crawl_url(url):
    return not url.startswith("https://maps.google.com") and not url.startswith("https://accounts.google.com")

def crawl(starting_url, regex, max_pages_to_crawl):

    is_hit, urls = crawl_single_page(starting_url, regex)
    all_urls = urls

    visited = set()
    hits = []
    
    while len(all_urls) != 0 and len(visited) < max_pages_to_crawl:

        url = all_urls.pop()

        if url in visited or not should_crawl_url(url):
            continue

        is_hit, urls = crawl_single_page(url, regex)

        visited.add(url)

        if is_hit:
            hits.append(url)
            all_urls.extend(urls)

    return hits

def get_search_suffix(human_readable_search):
    return human_readable_search.replace(" ", "+")

def get_google_query_url(search_base_url, human_readable_search):

    search_suffix = get_search_suffix(human_readable_search)
    return search_base_url + search_suffix

def output_hits(hits):
    output_file = open("hits.txt", "a")

    for i in range(0, len(hits)):
        hit = hits[i]
        print(hit)
        output_file.write(hit + "\n")

    output_file.close()

def main(search_base_url, human_readable_searches, regex, max_pages_to_crawl):

    for i in range(0, len(human_readable_searches)):

        human_readable_search = human_readable_searches[i]
        google_search_url = get_google_query_url(search_base_url, human_readable_search)

        hits = crawl(google_search_url, regex, max_pages_to_crawl)        
        output_hits(hits)

total_pages_crawled = 0
max_pages_to_crawl = 500
regex = "^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$"
regex = "trout"
human_readable_searches = ["yakima trout spots site:reddit.com"]
search_base_url = "https://www.google.com/search?q="

main(search_base_url, human_readable_searches, regex, max_pages_to_crawl)