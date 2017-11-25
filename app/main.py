import os
from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from app import create_app, db

app = create_app()


@app.route('/')
def index():
    return render_template('movies.html')


@app.route('/search/', methods=['POST'])
def search():
    data = request.data

    return render_template('search.html')


if __name__ == '__main__':
    app.run()
