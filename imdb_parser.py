from imdbpie import Imdb as imdb


class Movie():
    def __init__(self, info_dict, reviews):
        self.movie_info = info_dict
        self.reviews = reviews


def get_reviews_from_imdb(mov_id, max_res):
    rev_list = imdb.get_title_reviews(mov_id, max_res)
    for review in rev_list:
        if not review.rating:
            review.rating = 0
    rev_list = sorted(rev_list, key=lambda x: x.rating, reverse=True)
    return rev_list


def get_movies():
    imdb_movies = imdb.top_250()[:10]

    movies = []
    for i in range(len(imdb_movies)):
        imdb_movie = imdb_movies[i]
        movie = Movie(imdb_movie, get_reviews_from_imdb(imdb_movie['tconst'], 100))
        movies.append(movie)

    return movies