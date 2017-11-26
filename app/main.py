import os
from imdbpie import Imdb

from flask import Flask
from flask import render_template, request

from flask_pymongo import PyMongo
from models import Dmovie
import imdb_parser

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'emotive'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/emotive'

imdb = Imdb()
mongo = PyMongo(app)


def fill_movie_obj(db_m):
    mov = Dmovie()
    mov.id, mov.title, mov.url = db_m['id'], db_m['title'], db_m['url']
    mov.emojis, mov.rating, mov.year = db_m['emojis'], db_m['rating'], db_m['year']
    return mov


@app.route('/fill')
def fill():
    db = mongo.db.movies
    ms = imdb_parser.get_movies()
    for m in ms:
        emojis = ';'.join(m.emojis)
        db.insert({'id': m.index,
                   'title': m.title,
                   'url': m.data['image']['url'],
                   'emojis': emojis,
                   'rating': m.data['rating'],
                   'year': m.data['year']})

    return 'ok'


@app.route('/movie/<movie_id>')
def get_movie(movie_id):
    db_movies = mongo.db.movies
    db_m = db_movies.find_one({'id': movie_id})
    mov = fill_movie_obj(db_m)
    more_info = imdb.get_title_by_id(movie_id)
    more_info.emojis = mov.emojis.split(';')
    return render_template('movie.html', movie=more_info)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movies')
def movies():
    db_movies = mongo.db.movies
    movies = db_movies.find()
    res = []
    for db_m in movies:
        mov = fill_movie_obj(db_m)
        res.append(mov)
        print(db_m['title'])
    return render_template('movies.html', movies=res)


@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        data = request.args['string']
        emojis = set(data.split(','))
        db_movies = mongo.db.movies
        movies = db_movies.find()
        most_common = dict()
        for m in movies:
            db_em = set(m['emojis'].split(';'))
            inters = emojis.intersection(db_em)
            most_common[m['title']] = len(inters)
            print(len(inters))
        res = sorted(list(most_common.items()),
                     key=lambda x: x[1],
                     reverse=True)
        res_movies = []
        for m in res:
            db_m = mongo.db.movies.find_one({'title': m[0]})
            mov = fill_movie_obj(db_m)
            res_movies.append(mov)
        print(res)
        return render_template('search.html', movies=res_movies)


if __name__ == '__main__':
    app.run(debug=True)