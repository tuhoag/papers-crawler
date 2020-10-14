from dotenv import load_dotenv
import arcas
import os

load_dotenv(".env")

key = os.getenv("IEEE_KEY")

api = arcas.Ieee()
api.key_api = key

parameters = api.parameters_fix(title='cluster-based anonymization of directed graphs', records=1)
url = api.create_url_search(parameters)

request = api.make_request(url)
root = api.get_root(request)
raw_article = api.parse(root)
print(raw_article)
article = api.to_dataframe(raw_article[0])

print(article.columns)
print(article[["title", "author", "url"]])