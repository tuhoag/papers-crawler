import logging
import json

from scholarly import scholarly
import pandas as pd

logger = logging.getLogger(__name__)

def setup_logger(level):
    logger.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    logger.addHandler(ch)



def get_papers(file_path):
    raw_data = []

    with open(file_path) as f:
        data = json.load(f)
        papers_list = data['result']['hits']['hit']
        num_papers = len(papers_list)

        logger.info("num of papers: {}".format(num_papers))

        for paper_dict in papers_list:
            info = paper_dict['info']
            logger.debug("paper info: {}".format(info))
            title = info['title']
            logger.debug("paper title: {}".format(title))

            pages = info.get("pages")
            logger.debug("paper pages: {}".format(pages))

            if pages is None:
                continue

            splits = pages.split('-')
            if len(splits) <= 1:
                continue
            elif not splits[0].isnumeric():
                continue

            logger.debug(splits)
            start_page, end_page = map(int, splits)
            num_pages = end_page - start_page + 1

            logger.debug("num pages: {} ({} - {})".format(num_pages, start_page, end_page))

            year = int(info["year"])

            logger.debug(info["authors"]["author"])

            if isinstance(info["authors"]["author"], dict):
                authors_info = [info["authors"]["author"]]
            elif isinstance(info["authors"]["author"], list):
                authors_info = info["authors"]["author"]
            else:
                raise Exception("Unsupported author type: {}".format(info["authors"]["author"]))
            logger.debug("author is dict: {}".format(isinstance(info["authors"]["author"], dict)))
            logger.debug(authors_info)
            num_authors = len(authors_info)

            authors_list = list(map(lambda author_dict: author_dict["text"], authors_info))
            authors_str = ",".join(authors_list)
            # logger.info(info["authors"]["author"])
            logger.debug(authors_list)
            logger.debug(authors_str)
            # raise Exception()
            raw_data.append({
                "title": title,
                "num_pages": num_pages,
                "start_page": start_page,
                "end_page": end_page,
                "year": year,
                "num_authors": num_authors,
                "authors": authors_list,
            })

    return raw_data

def get_short_papers(papers_df, min_num_pages = 5, max_num_pages = 6):
    return list(filter(lambda item: min_num_pages <= item["num_pages"] <= max_num_pages, papers_df))

def update_cited_papers(papers_list):
    for paper_dict in papers_list:
        cited_papers = get_cited_paper_of_same_author(paper_dict)

def get_cited_paper_of_same_author(paper_dict):
    logger.info(paper_dict)
    search_query = scholarly.search_pubs(paper_dict["title"])
    for result in search_query:
        logger.info(result)

        for cited_paper in result.citedby:
            logger.info("cited paper: {}".format(cited_paper))

        bibtex = result.bibtex
        logger.info(bibtex)
        # logger.info(result.cites)

        raise Exception()


setup_logger(logging.INFO)
all_papers = get_papers("icde_papers.json")
short_papers = get_short_papers(all_papers)

logger.info("num of all papers: {}".format(len(all_papers)))
logger.info("num of short papers: {}".format(len(short_papers)))

update_cited_papers(short_papers)