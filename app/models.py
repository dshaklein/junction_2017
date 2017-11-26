from collections import defaultdict


class Dmovie:
    id = None
    title = None
    url = None
    emojis = None
    rating = None
    year = None

    def __repr__(self):
        return '<Movie %r>' % self.title
