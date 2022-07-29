import random
from constants import *
from assets_console import *
from maps.classic_console import *



### ----- VARIABLES ------ ###



# --- game --- #

game: Game = Game(classic_continents)


### ------ FUNCTIONS ------ ###



def addSpace() -> None:
    for _ in range(5):
        print()



### ------ CLASSES ------ ###



### ------ MAIN ------ ###



# --- cls --- #
addSpace()

# --- game setup --- #

# map #
assigning_territories: bool = True
empty_territories_left: bool = False

# aesthetics: print all players #

print("players: ", end=" [ ")
for player in game.getPlayers():
    if game.getPlayers().index(player) != len(game.getPlayers()) - 1:
        print(player.color, end=", ")
    else:
        print(player.color, "]")

# assign territories #
chosen_continent: Continent = random.choice(game.getContinentsList())
chosen_territory: Territory = random.choice(chosen_continent.getTerritoriesList())

while assigning_territories:

    # choose empty continent
    while not chosen_continent.hasEmptyTerritories():
        chosen_continent = random.choice(game.getContinentsList())
    
    # choose empty territory
    while not chosen_territory.isEmpty():
        chosen_territory = random.choice(chosen_continent.getTerritoriesList())
    
    chosen_territory.ruler = game.active_player      # assign ruler

    # check if there are any territories left
    empty_territories_left = True
    for continent in game.getContinentsList():
        if continent.hasEmptyTerritories():
            empty_territories_left = False
    
    assigning_territories = not empty_territories_left
    game.passTurn()

for player in game.getPlayers():
    print(f"{player.color} has: {game.countPlayerTerritories(player)} territories")

game.passPhase()
addSpace()

# --- end game --- #

print("game over")