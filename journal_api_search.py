import requests
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
import os
from dotenv import load_dotenv
import math

load_dotenv()

# print(os.environ.get("SCOPUS_KEY"))

## Initialize client
# client = ElsClient(os.environ.get("SCOPUS_KEY"))

# # doc_srch = ElsSearch("AUTHOR-NAME(hoang) AND PUBYEAR > 2011",'scopus')
# # doc_srch.execute(client, get_all = True)
# # print ("doc_srch has", len(doc_srch.results), "results.")

# doc_srch = ElsSearch("anonymization",'sciencedirect')
# doc_srch.execute(client, get_all = False)
# print ("doc_srch has", len(doc_srch.results), "results.")
# print(doc_srch.results)

# for data in doc_srch.results:
#     title = data["dc:title"]
#     authors = list(map(lambda item: item["$"], data["authors"]["author"]))
#     print(title)
#     print(authors)
#     print(data)

api_key = os.environ["SCOPUS_KEY"]

# resp = requests.get(api_key, headers={"Accept": "application/json", })

query_params = {
    "query": "ABS(knowledge and graph) AND TITLE(differential privacy)",
    "date": "2015-2021",
    "view": "COMPLETE",
    "DOCKTYPE": "(ar, cp)",
    # "title": "(differential)"
}
resp = requests.get("https://api.elsevier.com/content/search/scopus",
                    headers={'Accept':'application/json', 'X-ELS-APIKey': api_key}, params=query_params)
json_result = resp.json()
search_results = json_result["search-results"]

print(search_results.keys())
# print(search_results["link"])
total_results = int(search_results["opensearch:totalResults"])
start_index = int(search_results["opensearch:startIndex"])
items_per_page = int(search_results["opensearch:itemsPerPage"])
num_pages = math.ceil(total_results / items_per_page)
print("page {}/{}: found {}/{} results".format(start_index, num_pages, items_per_page, total_results))



found_documents = search_results["entry"]
for idx, document in enumerate(found_documents):
    print(idx)
    print(document["dc:title"])
    print(document["prism:publicationName"])
    print(document["prism:pageRange"])
    print(document["prism:coverDisplayDate"])
    print(document.get("authkeywords"))
    print(document["dc:description"])
