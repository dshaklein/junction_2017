import the_model
from collections import defaultdict


class Movie:

    def __init__(self, index):
        self.index = index
        self.title = None
        self.relevant_percent = 0.5
        self.reviews = None
        self.emojis = set()
        self._emojis_counter = defaultdict(int)

    def calc_proc(self, freq):
        sum = 0
        for key, value in freq:
            sum += value
        res = [(key, round(value / sum * 100, 1)) for key, value in freq]
        return res

    def calc_emojis(self):
        if self.reviews:
            em_freq = the_model.text_to_emoji(self.reviews)
            res = self.calc_proc(em_freq)
        else:
            res = []
        print(self.title, res)
