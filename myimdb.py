from imdbpie import Imdb
imdb = Imdb()
imdb = Imdb(anonymize=True) # to proxy requests

reviews = imdb.get_title_reviews("tt0468569", max_results=100)
reviews_s = sorted(reviews, key=lambda x: x.rating, reverse=True)[:20]
print(reviews_s)
print(1)