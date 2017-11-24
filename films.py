from collections import defaultdict
from analizer import get_emoji
from reviews import get_reviews


class Film:

    def __init__(self, index):
        self.index = index
        self.relevant_percent = 0.5
        self.reviews = None
        self.emojis = set()
        self._emojis_counter = defaultdict(int)
        self.run()

    def run(self):
        self.reviews = get_reviews(self.index)
        for review in self.reviews:
            emoji = get_emoji(review.text)
            self._emojis_counter[emoji] += 1

    def get_relevant_emojis(self):
        em_list = self._emojis_counter.items()
        em_sorted = sorted(em_list, lambda x: x[1], reverse=True)
        relevant_em_count = int(self.relevant_percent * len(em_sorted))
        ems = em_sorted[:relevant_em_count]
        for key, val in ems:
            self.emojis.add(key)

