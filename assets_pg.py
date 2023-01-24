import pygame as pg
from pygame.locals import *
import tkinter as tk
from constants import *
import random
import time


class TerritoryCard:
    
    def __init__(self, design: str) -> None:
        
        self.design: str = design
    
    ### SETTERS ###
    
    ### GETTERS ###
    
    def getDesign(self) -> str:
        return self.design
    
    ### ACTIONS ###
    
    def isNull(self) -> bool:
        return self.design == "n"


class Player:

    def __init__(self, player_color: str, is_null: bool = False) -> None:
        
        self.null_type: bool = is_null

        # geography #
        self.color: str = player_color
        
        # military #
        self.available_troops: int = 0
        
        # territory cards #
        self.territory_cards: list[TerritoryCard] = []

    ### SETTERS ###

    def setColor(self, new_color: str) -> None:
        self.color = new_color
    
    def setTroops(self, number_troops: int) -> None:
        self.available_troops = number_troops

    def addTroops(self, number_troops: int) -> None:
        self.available_troops += number_troops

    def removeTroops(self, number_troops: int) -> None:
        self.available_troops -= number_troops
    
    def addTerritoryCard(self, new_card: TerritoryCard) -> None:
        self.territory_cards.append(new_card)
    
    def addRandomTerritoryCard(self) -> None:
        self.addTerritoryCard(TerritoryCard(random.choice(TERRITORY_CARD_DESIGNS)))
    
    def removeTerritoryCard(self, given_card: TerritoryCard) -> None:
        
        if given_card not in self.territory_cards:
            card_type: str = "infantry"
            if given_card.getDesign() == "c":
                card_type = "cavalry"
            elif given_card.getDesign() == "a":
                card_type = "artillery"
            elif given_card.getDesign() == "w":
                card_type = "wild card"
            raise Exception(f"{self.color} player has no card of type {card_type}")
        
        self.territory_cards.remove(given_card)
    
    ### GETTERS ###
    
    def isNull(self) -> bool:
        return self.null_type

    def getColor(self) -> str:
        return self.color
    
    def getTroops(self) -> int:
        return self.available_troops
    
    def getTerritoryCards(self) -> list[TerritoryCard]:
        return self.territory_cards
    
    ### ACTIONS ###

    def printTerritoryCards(self) -> None:
        for card in self.territory_cards:
            if self.territory_cards.index(card) != len(self.territory_cards) - 1:
                print(card.design.upper(), end = ", ")
            else:
                print(card.design.upper())
    
    
class Territory:

    def __init__(self, name: str = "", territory_id: str = "", neighbours = None, x: int = 0, y: int = 0,
                 is_null: bool = False) -> None:
        
        self.null_type: bool = is_null
        
        if neighbours is None:
            neighbours = []
        
        # geography #
        self.x: int = x
        self.y: int = y

        self.name: str = name
        self.id: str = territory_id

        self.ruler = NULL_PLAYER
        self.neighbours: list[str] = neighbours

        # military #
        self.troops_stationed = 0
    
    ### SETTERS ###
    
    def setCoords(self, new_x: int, new_y: int) -> None:
        self.x = new_x
        self.y = new_y
    
    def setID(self, territory_id: str) -> None:
        self.id = territory_id

    def setRuler(self, new_ruler: Player) -> None:
        self.ruler = new_ruler
    
    def setTroops(self, number_troops: int) -> None:
        self.troops_stationed = number_troops

    def addTroops(self, number_troops: int) -> None:
        self.troops_stationed += number_troops

    def removeTroops(self, number_troops: int) -> None:
        self.troops_stationed -= number_troops
    
    def removeTroop(self) -> None:
        self.removeTroops(1)

    ### GETTERS ###

    def isNull(self) -> bool:
        return self.null_type
    
    def getCoords(self) -> tuple[int, int]:
        return self.x, self.y
    
    def getName(self) -> str:
        return self.name
    
    def getID(self) -> str:
        return self.id

    def getRuler(self) -> Player:
        return self.ruler
    
    def getNeighbours(self) -> list[str]:
        return self.neighbours
    
    def getTroops(self) -> int:
        return self.troops_stationed
    
    ### ACTIONS ###

    def draw(self, screen: pg.Surface) -> None:
        # territory marker
        pg.draw.circle(screen, Color(self.ruler.color), (self.x, self.y), TERRITORY_MARKER_RADIUS)
        
        # territory troops
        font: pg.font.Font = pg.font.Font(None, 4*FONT_SIZE//5)
        text_color: str = "black"
        if self.ruler.color in DARK_COLORS:
            text_color = "white"
        troops_text = font.render(str(self.troops_stationed), True, text_color)
        troops_text_rect = troops_text.get_rect(center = (self.x, self.y))
        screen.blit(troops_text, troops_text_rect)
    
    def isEmpty(self) -> bool:
        return self.ruler.isNull()


class Continent:

    def __init__(self, name: str = "n/a", continent_id: str = "", territories: dict[str: Territory] | None = None, bonus_troops: int = 0,
                 is_null: bool = False) -> None:
        
        self.null_type: bool = is_null
        if territories is None:
            territories = {}
        
        # geography #
        self.name: str = name
        self.id: str = continent_id
        self.territories: dict[str: Territory] = territories
        
        self.territories_list: list[Territory] = []
        for territory in self.territories.values():
            self.territories_list.append(territory)

        self.ruler: Player = NULL_PLAYER

        # military #
        self.bonus_troops: int = bonus_troops
    
    ### SETTERS ###
    
    def setID(self, new_id) -> None:
        self.id = new_id
    
    def setRuler(self, new_ruler: Player) -> None:
        self.ruler = new_ruler
    
    def setBonusTroops(self, bonus_troops: int) -> None:
        self.bonus_troops = bonus_troops
    
    ### GETTERS ###

    def isNull(self) -> bool:
        return self.null_type
    
    def getName(self) -> str:
        return self.name

    def getID(self) -> str:
        return self.id
    
    def getTerritories(self) -> dict[str: Territory]:
        return self.territories

    def getTerritoriesList(self) -> list[Territory]:
        return self.territories_list

    def getRuler(self) -> Player:
        if self.hasSingleRuler():
            return self.territories_list[0].ruler
        return NULL_PLAYER
    
    def getBonusTroops(self) -> int:
        return self.bonus_troops

    ### ACTIONS ###

    def drawTerritories(self, screen: pg.Surface):
        for territory in self.getTerritoriesList():
            territory.draw(screen)

    def findTerritory(self, territory_id: str) -> Territory:
        if territory_id in self.territories.keys():
            return self.territories[territory_id]
        return NULL_TERRITORY
    
    def hasEmptyTerritories(self) -> bool:
        for territory in self.getTerritoriesList():
            if territory.isEmpty():
                return True
        return False
    
    def hasSingleRuler(self) -> bool:
        ruler: Player = self.territories_list[0].ruler    # doesn't matter which one, if they all have the same ruler

        for territory in self.territories_list:
            if territory.getRuler() != ruler:
                return False
        
        return True

    def countTerritories(self) -> int:
        return len(self.getTerritoriesList())


class Game:

    def __init__(self, map_image: pg.image, continents: dict[str: Continent]) -> None:
        
        print("commencing game setup...\n")
        
        # players #
        self.players: list[Player] = []
        self.active_player: Player = NULL_PLAYER

        # dice #
        self.dice: list[list[int]] = [[0, 0], [0, 0, 0]]

        # map #
        self.map: pg.image = pg.transform.scale(map_image, (WIDTH, HEIGHT))
        self.continents: dict[str: Continent] = continents
        self.continents_list: list[Continent] = []

        for continent in self.continents.values():
            self.continents_list.append(continent)

        # territory cards #
        self.territory_cards_window: bool = False  # True when player is viewing their territory cards
        self.player_received_card: bool = False
        self.trades_completed: int = 0      # amount of trades players have made
        self.territory_cards_overflow: bool = False     # player has > 5 territory cards
        
        # game #
        self.phase: int = 0
        self.first_territory: Territory = NULL_TERRITORY      # territory from which an attack will be launched

        # init #
        self.create_players()
        self.assignTerritories()
        self.autoSetupTroops()
        self.passPhase()
        
        print("starting game...")
        time.sleep(2)
    
    ### SETTERS ###

    def setFirstTerritory(self, territory: Territory) -> None:
        self.first_territory = territory
    
    def rollDice(self) -> None:
        for role in range(len(self.dice)):
            for dice in range(len(self.dice[role])):
                self.dice[role][dice] = random.randint(1, 6)
            self.dice[role].sort()
            self.dice[role].reverse()
    
    def toggleTerritoryCardsWindow(self) -> None:
        self.territory_cards_window = not self.territory_cards_window
    
    def receiveCard(self) -> None:
        self.player_received_card = True
        self.active_player.addRandomTerritoryCard()
    
    def addTrade(self) -> None:
        self.trades_completed += 1
    
    def toggleTerritoryCardsOverflow(self) -> None:
        self.territory_cards_overflow = not self.territory_cards_overflow
    
    ### GETTERS ###

    def getPlayers(self) -> list[Player]:
        return self.players
    
    def getContinents(self) -> dict[str: Continent]:
        return self.continents
    
    def getContinentsList(self) -> list[Continent]:        
        return self.continents_list
    
    def isViewingTerritoryCards(self) -> bool:
        return self.territory_cards_window
    
    def playerHasReceivedCard(self) -> bool:
        return self.player_received_card
    
    def getTrades(self) -> int:
        return self.trades_completed
    
    def hasTerritoryCardOverflow(self) -> bool:
        return self.territory_cards_overflow
    
    def getPhaseStr(self) -> str:   # get phase as a string
        return PHASE_NAMES[self.phase - 1]
    
    def hasSelectedFirstTerritory(self) -> bool:
        return not self.first_territory.isNull()

    ### ACTIONS ###

    # --- players --- #
    
    def create_players(self) -> None:
        
        print("creating players...")
        
        # select number of players #
        user_input: str = input("enter the number of players (3-6): ")

        # check valid input
        while user_input not in "3456":

            if user_input not in "012789":
                user_input = input(f"'{user_input}' is of invalid format. Please enter a number in the range of [3; 6]: ")
                continue

            user_input = input(f"'{user_input}' is an invalid number of players. Please enter a number in the range [3; 6]: ")

        # auto choose players #
        if user_input == '':
            user_input = '4'
            print(f"player count was randomly set to {user_input}")

        n_players = int(user_input)

        print()
        
        available_colors: list[str] = ["green", "red", "blue", "dimgrey", "orange", "purple"]
        color: str

        for i in range(n_players):

            # choose player color >>>
            if len(available_colors) == 1:      # there is only 1 color left
                color = available_colors[0]
                print(f"player {n_players}'s color was set to {color} as it was the only one left")
            else:
                color = input(f"choose color for player {i + 1} (available: {available_colors}): ").lower()
            # <<<
            
            # auto choose color #
            if color == '':
                color = random.choice(available_colors)
                print(f"player {i + 1}'s color was randomly set to {color}")

            # check color availability >>>
            while color not in available_colors:
                color = input(f"color not available, choose one of {available_colors}: ")
            # <<<
            
            available_colors.remove(color)          # update available colors
            self.players.append(Player(color))      # add player
        
        self.active_player = self.players[random.randint(0, len(self.players) - 1)]     # assign random player as starting player
        
        print("players created\n")

    def passTurn(self) -> None:
        player_turn: int = self.players.index(self.active_player)
        player_turn += 1
        if player_turn == len(self.players):
            player_turn = 0
        self.active_player = self.players[player_turn]
        self.player_received_card = False   # reset
        
    def countPlayerTerritories(self, player: Player) -> int:

        count: int = 0

        for continent in self.getContinentsList():
            for territory in continent.getTerritoriesList():
                if territory.ruler == player:
                    count += 1
        
        return count

    def getPlayerTerritories(self, player: Player) -> list[Territory]:
        
        territories: list[Territory] = []
        
        for continent in self.getContinentsList():
            for territory in continent.getTerritoriesList():
                if territory.ruler.color == player.color:
                    territories.append(territory)
        
        return territories
    
    def calculateDraftTroops(self, player: Player) -> int:
        draft_troops: int = 3   # by default, player gets 3 troops
        
        # bonus troops for number of territories owned >>>
        territories_owned: int = self.countPlayerTerritories(player)
        if territories_owned >= 12:
            draft_troops += territories_owned//3 - 3
        # <<<

        # bonus troops for ruling entire continents >>>
        for continent in self.continents_list:
            if continent.getRuler() == player:
                draft_troops += continent.bonus_troops
        # <<<

        return draft_troops
    
    def trade_troops(self) -> None:
        
        troops_gained: int
        
        if self.trades_completed < len(FIRST_TRADES_TROOPS):
            troops_gained = FIRST_TRADES_TROOPS[self.trades_completed]
        else:
            troops_gained = 5 * (self.trades_completed - 2)     # 6 trades -> 20 troops, 7 trades -> 25 troops, ...
        
        self.active_player.addTroops(troops_gained)
        self.trades_completed += 1
    
    # --- map --- #

    def assignTerritories(self) -> None:
        
        print("assigning territories...")
        
        chosen_continent: Continent = random.choice(self.getContinentsList())
        chosen_territory: Territory = random.choice(chosen_continent.getTerritoriesList())

        assigning_territories: bool = True
        empty_territories_left: bool

        while assigning_territories:

            # choose empty continent
            while not chosen_continent.hasEmptyTerritories():
                chosen_continent = random.choice(self.getContinentsList())
            
            # choose empty territory
            while not chosen_territory.isEmpty():
                chosen_territory = random.choice(chosen_continent.getTerritoriesList())
            
            # assign territory
            chosen_territory.ruler = self.active_player      # assign ruler
            chosen_territory.addTroops(1)       # every territory needs to have at least 1 troop

            # check if there are any territories left
            empty_territories_left = True
            for continent in self.getContinentsList():
                if continent.hasEmptyTerritories():
                    empty_territories_left = False
            
            assigning_territories = not empty_territories_left
            self.passTurn()
        
        print("territories assigned\n")

    def autoSetupTroops(self) -> None:
        
        print("placing random troops...")
    
        for player in self.players:
            # for 3 players, 35 troops per player
            # for 4 players, 30 troops per player
            # for 5 players, 25 troops per player
            # for 6 players, 20 troops per player
            # 1 troop has already been placed when assigning territories
            player.setTroops(35 - (len(self.players) - 3) * 5 - 1)
            player_territories: list[Territory] = self.getPlayerTerritories(player)
            while player.getTroops() != 0:
                # select random territory owned by 'player' and add random amount of troops out of those remaining
                # for balancing purposes, avoid placing too many troops on a single territory >
                troops_placed = random.randint(1, min(3, player.getTroops()))
                random.choice(player_territories).addTroops(troops_placed)
                player.removeTroops(troops_placed)
        
        print("troops placed\n")
    
    def drawTerritories(self, screen: pg.Surface) -> None:
        for continent in self.continents_list:
            continent.drawTerritories(screen)

    def findTerritory(self, territory_id: str) -> Territory:
        for continent in self.getContinentsList():
            territory = continent.findTerritory(territory_id)
            if not territory.isNull():
                return territory
        return NULL_TERRITORY

    def findTerritoryContinent(self, territory_id: str) -> Continent:
        for continent in self.getContinentsList():
            territory = continent.findTerritory(territory_id)
            if not territory.isNull():
                return continent
        return NULL_CONTINENT
    
    def findContinent(self, continent_id: str) -> Continent:
        if continent_id in self.getContinents().keys():
            return self.getContinents()[continent_id]
        return NULL_CONTINENT
    
    def getLargestContinent(self) -> Continent:
        largest_continent: Continent = NULL_CONTINENT
        for continent in self.getContinentsList():
            if len(continent.getTerritoriesList()) > len(largest_continent.getTerritoriesList()):
                largest_continent = continent
        return largest_continent
    
    def countTerritories(self) -> int:
        count: int = 0
        for continent in self.getContinentsList():
            count += continent.countTerritories()
        return count
    
    def selectTerritory(self, click_coords: tuple[int, int]) -> Territory:

        """
        can be made faster by reducing each continent to a rectangle and then finding which rectangle was clicked,
        thus instantly knowing which continent was clicked
        """

        for continent in self.continents_list:
            for territory in continent.territories_list:
                if abs(territory.x - click_coords[0]) <= TERRITORY_MARKER_RADIUS:   # check x-coord
                    if abs(territory.y - click_coords[1]) <= TERRITORY_MARKER_RADIUS:   # check y-coord
                        return territory
        
        return NULL_TERRITORY
    
    # --- game --- #

    def passPhase(self) -> None:
        
        self.first_territory = NULL_TERRITORY       # reset at the end of phase
        self.phase += 1
        
        if self.phase == 4:     # there are only 3 phases: draft, attack, fortify
            self.phase = 1
            self.passTurn()     # at the end of phase 3, it is the next player's turn

        if self.phase == 1:
            # add drafting troops #
            self.active_player.setTroops(self.calculateDraftTroops(self.active_player))

    def askTroops(self, purpose: str) -> int:
        
        troops: int = 0  # input (can't get input after .destroy())
    
        master: tk.Tk = tk.Tk()  # create window
        master.title(self.getPhaseStr())
        tk.Label(master, text = purpose).grid(row = 0, column = 0)  # info text
        troops_field: tk.Entry = tk.Entry(master)  # input field
        troops_field.grid(row = 0, column = 1)
        tk.Button(master, text = "confirm", command = master.quit).grid(row = 1)    # confirmation button
        tk.mainloop()
        if troops_field.get() != "":  # no value given
            troops = int(troops_field.get())
        master.destroy()  # close window
        return troops

    def draftTroops(self) -> None:
    
        troops_drafted: int = 1     # default
        
        if self.active_player.getTroops() != 1:     # if more than 1 troop left to draft
            # ask how many troops should be drafted >
            troops_drafted = self.askTroops(f"troops drafted to {self.first_territory.name}: ")
            # check that the given number doesn't exceed the max >
            troops_drafted = min(troops_drafted, self.active_player.available_troops)
            # check that the given number isn't negative >
            troops_drafted = max(0, troops_drafted)
    
        # draft troops >>>
        self.first_territory.addTroops(troops_drafted)
        self.active_player.removeTroops(troops_drafted)
        # <<<
    
    def conquerTerritory(self, territory_conquered: Territory, conqueror: Player) -> None:
        if self.countPlayerTerritories(territory_conquered.ruler) == 1:     # this was the enemy player's last territory -> remove player from the game
            for territory_card in territory_conquered.ruler.getTerritoryCards():    # conqueror inherits all territory cards held by defeated opponent
                conqueror.addTerritoryCard(territory_card)
            if len(conqueror.getTerritoryCards()) > 4:     # player can't hold more than 4 cards
                self.phase = 1
                self.territory_cards_overflow = True
            self.players.remove(territory_conquered.ruler)
        territory_conquered.setRuler(conqueror)     # update ruler

    def attack(self, defending_territory: Territory) -> None:

        attacking_troops: int
        defending_troops: int

        # keep attack going until 1 army is defeated
        while defending_territory.getTroops() > 0 and self.first_territory.getTroops() > 1:
            
            attacking_troops = self.first_territory.getTroops()
            defending_troops = defending_territory.getTroops()

            self.rollDice()
            
            # remove troops based on dice roll >>>
            # number of battles depends on lowest number of troops >
            for battle in range(min(min(defending_troops, 2), min(attacking_troops - 1, 3))):
                if self.dice[0][battle] >= self.dice[1][battle]:   # defence wins battle
                    self.first_territory.removeTroop()
                else:
                    defending_territory.removeTroop()
            # <<<
            
            # print dice roll >>>
            print(f"\n{self.first_territory.name} rolled {self.dice[1]}")
            print(f"{defending_territory.name} rolled {self.dice[0]}")
            # <<<
        
        print()
    
    # move troops stationed after a successful attack
    def advanceTroops(self, territory_conquered: Territory) -> None:
        
        # set new ruler >
        self.conquerTerritory(territory_conquered, self.active_player)
    
        # determine how many troops should be carried over >>>
        troops_moved: int = self.first_territory.getTroops() - 1  # if attacking territory only has 2 to 4 troops left, moving all but one troop is the only option
        if self.first_territory.getTroops() > 4:  # common case (troops left in attacking territory is > 4)
            # player can decide how many troops they want to carry over >
            troops_moved = self.askTroops(f"troops advancing from {self.first_territory.name} to {territory_conquered.name}")
            # check validity of 'troops_moved' (>= 1 troop must stay behind; non-negative; >= 3 troops need to be carried over) >
            troops_moved = max(min(troops_moved, self.first_territory.getTroops() - 1), 3)
        # <<<
    
        territory_conquered.setTroops(troops_moved)  # carry over troops from attacking territory to conquered territory
        self.first_territory.removeTroops(troops_moved)  # leave behind remaining troops
        self.setFirstTerritory(territory_conquered)  # move player to next territory
    
    def fortify(self, destination: Territory) -> None:
        
        troops_moved: int = 1    # default
        
        if self.first_territory.getTroops() > 2:       # if more than 1 troop can be moved
            troops_moved: int = self.askTroops(f"troops to be moved from {self.first_territory.name} to {destination.name}")
            # check that the input number is valid
            troops_moved = min(max(troops_moved, 0), self.first_territory.troops_stationed - 1)
        
        # fortify
        if troops_moved != 0:   # redundancy
            self.first_territory.removeTroops(troops_moved)
            destination.addTroops(troops_moved)
            self.passPhase()    # can only fortify once


# NULL OBJECTS #

NULL_PLAYER: Player = Player("n/a", True)
NULL_TERRITORY: Territory = Territory(is_null = True)
NULL_CONTINENT: Continent = Continent(is_null = True)

# TERRITORY CARDS #

TERRITORY_CARD_DESIGNS: list[str] = ["i", "c", "a", "w"]
INFANTRY_CARD: TerritoryCard = TerritoryCard(TERRITORY_CARD_DESIGNS[0])
CAVALRY_CARD: TerritoryCard = TerritoryCard(TERRITORY_CARD_DESIGNS[1])
ARTILLERY_CARD: TerritoryCard = TerritoryCard(TERRITORY_CARD_DESIGNS[2])
WILD_CARD: TerritoryCard = TerritoryCard(TERRITORY_CARD_DESIGNS[3])
NULL_TERRITORY_CARD: TerritoryCard = TerritoryCard("n")
