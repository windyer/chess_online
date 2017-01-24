import random

from card.core.util import segment_tree
from card.core.conf import settings
from card.core.enum import RouletteType

class RouletteProbController(object):

    _instance = None

    def __init__(self, sample=settings.ROULETTE.sample):
        self._free_stree = None
        self._pay_stree = None
        self._sample = sample

    @staticmethod
    def get_random(roulette_type):
        if RouletteProbController._instance == None:
            RouletteProbController._instance = RouletteProbController()
        luck_num = random.randrange(1, settings.ROULETTE.sample)
        return RouletteProbController._instance.search(luck_num, roulette_type)

    def search(self, value, roulette_type):
        if RouletteType.FREE == roulette_type:
            if self._free_stree is None:
                self._load_free_data()
            return self._free_stree.search(value)
        if self._pay_stree is None:
            self._load_pay_data()
        return self._pay_stree.search(value)

    def list_item(self, roulette_type):
        if RouletteType.FREE == roulette_type:
            tree = self._free_stree
        else:
            tree = self._pay_stree
        for tree_item in tree.middle():
            print tree_item.key

    def _load_free_data(self):
        self._free_stree = segment_tree.SegmentTree()
        _prev = 0

        for roulette_item in self._get_free_data():
            if roulette_item.probability <= 0:
                continue
            _range = roulette_item.probability * self._sample + _prev
            _range = int(_range)
            self._free_stree.insert(roulette_item, _prev, _range)
            _prev = _range

    def _get_free_data(self):
        for item in settings.ROULETTE.roulette_items:
            yield item

    def _load_pay_data(self):
        self._pay_stree = segment_tree.SegmentTree()
        _prev = 0

        for roulette_item in self._get_pay_data():
            if roulette_item.probability <= 0:
                continue
            _range = roulette_item.probability * self._sample + _prev
            _range = int(_range)
            self._pay_stree.insert(roulette_item, _prev, _range)
            _prev = _range

    def _get_pay_data(self):
        for item in settings.ROULETTE.currency_roulette_items:
            yield item