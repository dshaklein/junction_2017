from imdbpie import Imdb

from views import Movie
from main import mongo


imdb = Imdb()


def get_reviews_from_imdb(mov_id, max_res):
    rev_list = imdb.get_title_reviews(mov_id, max_res)
    if rev_list is None:
        return []
    for review in rev_list:
        if not review.rating:
            review.rating = 0
    rev_list = sorted(rev_list, key=lambda x: x.rating, reverse=True)
    return rev_list[:100]


def get_movies():

    imdb_movies = imdb.top_250()[:20]
    movies = []
    for mov in imdb_movies:
        # for popular
        # mov = mov['object']
        # for top 250

        movie = Movie(mov['tconst'], mov)
        more_info = imdb.get_title_by_id(mov['tconst'])

        movie.title = mov['title']
        movie.reviews = get_reviews_from_imdb(movie.index, 1000)
        movie.calc_emojis()
        movies.append(movie)
    return movies


if __name__ == '__main__':
    db = mongo.db.movies
    ms = get_movies()
    for m in ms:
        emojis = ';'.join(m.emojis)
        db.insert({'id': m.index,
                   'title': m.title,
                   'url': m.data['image']['url'],
                   'emojis': emojis})