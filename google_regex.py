# import module
import requests
import bs4

def execute_google_search(search_query):
    request_result = requests.get( search_query )

def get_search_suffix(human_readable_search):
    return human_readable_search.replace(" ", "+")

def get_google_query_url(human_readable_search):
    search_suffix = get_search_suffix(human_readable_search)

    return search_base_url + search_suffix

def output_hits(hits):
    output_file = open("hits.txt", "a")

    for i in range(0, len(hits)):
        hit = hits[i]
        print(hit)
        output_file.write(hit + "\n")

    output_file.close()

def main():

    for i in range(0, len(human_readable_searches)):
        human_readable_search = human_readable_searches[i]
        
        google_query_url = get_google_query_url(search_base_url, human_readable_search)
        google_search_results = execute_google_search(google_query_url)

        hits = crawl_and_compare()

        output_hits(hits)

regex = ""
human_readable_searches = ["yakima spots", "yakima river access", "yakima trout site:reddit.com"]
search_base_url = "https://www.google.com/search?q="

main()