from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('movies.html')



@app.route('/search/', methods=['POST'])
def search():
    data = request.data

    return render_template('search.html')

@app.route('')

if __name__ == '__main__':
    app.run()
