__author__ = 'IN'
from ge_game import GE_Game_random

def test_vector():
    invector = r'..\vectors\airport.shp'
    game = GE_Game_random(invector)
    game.make_point_series()
    assert game.nfeatures