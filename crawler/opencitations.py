import logging
import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://opencitations.net/index/coci/api/v1/{suburl}"
METADATA_URL = "metadata/{doi}"
CITATIONS_URL = "citations/{doi}"

def get_metadata(doi):
    """
    Gets metadata of a paper from its doi.
    """
    relative_url = METADATA_URL.format(doi=doi)
    full_url = BASE_URL.format(suburl=relative_url)

    result = requests.get(full_url)
    if result.status_code != 200:
        raise Exception('GET /{}: {}'.format(full_url, result.status_code))

    data = result.json()

    return data[0]


def get_citations(doi):
    """
    Gets citations of a paper from its doi.
    """
    relative_url = CITATIONS_URL.format(doi=doi)
    full_url = BASE_URL.format(suburl=relative_url)

    result = requests.get(full_url)
    if result.status_code != 200:
        raise Exception('GET /{}: {}'.format(full_url, result.status_code))

    data = result.json()

    print(data)
    raise Exception()
    return data[0]
