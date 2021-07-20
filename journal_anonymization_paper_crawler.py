import pandas as pd
import json
import requests
from lxml import etree
from urllib.parse import urlparse
from tqdm import tqdm
from joblib import Parallel, delayed


DBLP_PAPERS_SEARCH_API = "https://dblp.org/search/publ/api"

venue2ids = {
    "TOPS": ["ACM_Trans._Priv._Secur.", "ACM_Trans._Inf._Syst._Secur."],
    "TKDE": ["IEEE_Trans._Knowl._Data_Eng."]
}


def parser_paper_info_from_acm_website(html_text):
    paper_info = {}

    tree = etree.HTML(html_text)

    abstract_tags = tree.xpath("//div[contains(@class, 'abstractSection abstractInFull')]//p")
    if len(abstract_tags) > 0:
        paper_info["abstract"] = etree.tostring(abstract_tags[0], pretty_print=True, encoding="unicode")
    # else:

    #     with open("error.html", "w") as f:
    #         f.write(html_text)

        # raise Exception("cannot find abstract: {}".format(abstract_tags))

    keywords = []
    for level in range(1,4):
        terms_tags = tree.xpath("//ol[contains(@class, 'rlist level-{}')]//a".format(level))

        if len(terms_tags) > 1:
            keywords.append(list(terms_tags[0].itertext())[0])

    paper_info["keywords"]=keywords
    return paper_info

def parser_paper_info_from_ieee_website(html_text):
    start_index = html_text.find("\"userInfo\"")

    parathesis_count = 1
    content = "{"
    while(parathesis_count > 0 and start_index < len(html_text)):
        if html_text[start_index] == "{":
            parathesis_count += 1
        elif html_text[start_index] == "}":
            parathesis_count -= 1

        content += html_text[start_index]

        start_index += 1

    json_data = json.loads(json.loads(json.dumps(content)))

    paper_info = {}

    keyword_str = ""


    if "keywords" in json_data:
        for keyword_info in json_data["keywords"]:
            if keyword_info["type"] == "IEEE Keywords":
                keyword_str = ",".join(keyword_info["kwd"])
                break

        paper_info["keywords"] = keyword_str
    paper_info["abstract"] = json_data["abstract"]

    return paper_info

def get_paper_info_from_publisher(url):
    paper_info = {}

    response = requests.get(url)

    domain = urlparse(response.url).netloc

    if domain == "dl.acm.org":
        # it is ACM publisher
        paper_info = parser_paper_info_from_acm_website(response.text)
    elif domain == "ieeexplore.ieee.org":
        paper_info = parser_paper_info_from_ieee_website(response.text)
    else:
        raise Exception("Unsupported domain: {}".format(domain))


    # print(paper_info)
    return paper_info

def extract_paper_info_from_info(info, venue_name):
    paper = {}

    if type(info["info"]["authors"]["author"]) is list:
        author_str = ",".join([author["text"] for author in info["info"]["authors"]["author"]])
    else:
        author_str = info["info"]["authors"]["author"]["text"]

    paper["title"] = info["info"]["title"]
    paper["authors"] = author_str
    paper["url"] = info["info"]["ee"]
    paper["venue"] = venue_name
    paper["year"] = info["info"]["year"]

    # extra_info =
    paper.update(get_paper_info_from_publisher(paper["url"]))

    return paper



def get_papers_from_dblp():
    papers = []

    for venue_name, venue_ids in venue2ids.items():
        venue_search_param = "|".join(["venue:{}:".format(venue_id) for venue_id in venue_ids])

        json_result = requests.get(DBLP_PAPERS_SEARCH_API, params={"q": venue_search_param, "format":"json", "h":10000}).json()


        results = Parallel(n_jobs=2)(
            delayed(extract_paper_info_from_info)(info, venue_name) for info in tqdm(json_result["result"]["hits"]["hit"]))

        papers.extend(results)
        # print(results)
        # raise Exception()
        # for info in tqdm(json_result["result"]["hits"]["hit"]):
        #     papers.append(extract_paper_info_from_info(info, venue_name))

    # print(papers)
    return papers

def write_to_csv(papers):
    df = pd.DataFrame(papers)
    df.to_csv("anonymization.csv")

def main():
    venues = []

    papers = get_papers_from_dblp()
    print("crawled {} papers".format(len(papers)))

    write_to_csv(papers)


if __name__ == "__main__":
    main()