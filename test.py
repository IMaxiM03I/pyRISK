from assets_pg import *
from maps.classic_pg import *

game = Game(classic_continents)

game.rollDice()
print(f"{game.dice = }")