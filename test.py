from scholarly import scholarly
print(next(scholarly.search_author('Steven A. Cholewiak')))

# Retrieve the author's data, fill-in, and print
search_query = scholarly.search_author('Steven A. Cholewiak')
author = next(search_query).fill()
print(author)

# Print the titles of the author's publications
print([pub.bib['title'] for pub in author.publications])

# Take a closer look at the first publication
pub = author.publications[0].fill()
print(pub)

# Which papers cited that publication?
for cited_paper in pub.citedby:
    print(cited_paper)
    raise Exception()
# print([citation.bib['title'] for citation in ])

# What is the Bibtex of that publication?
# print(pub.bibtex)