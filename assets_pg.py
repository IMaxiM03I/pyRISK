import pygame as pg
from pygame.locals import *
from constants import *
import random


class Player:

    def __init__(self, player_color: str) -> None:

        # geography #
        self.color: str = player_color
        
        # military #
        self.available_troops: int = 0

    ### SETTERS ###

    def setColor(self, new_color: str) -> None:
        self.color = new_color
    
    def setTroops(self, number_troops: int) -> None:
        self.available_troops = number_troops

    def addTroops(self, number_troops: int) -> None:
        self.available_troops += number_troops

    def removeTroops(self, number_troops: int) -> None:
        self.available_troops -= number_troops
    
    ### GETTERS ###

    def getColor(self) -> str:
        return self.color
    
    def getTroops(self) -> int:
        return self.available_troops
    
    ### ACTIONS ###

    # def conquer(self, territory_conquered: Territory, troops_transfered: int) -> None:
    #     territory_conquered.ruler = self
    #     territory_conquered.addTroops(troops_transfered)


class Territory:

    def __init__(self, name: str = "", id: str = "", neighbours: list[str] = [], x:int = 0, y:int = 0) -> None:

        # geography #
        self.x: int = x
        self.y: int = y

        self.name: str = name
        self.id: str = id

        self.ruler = None
        self.neighbours: list[str] = neighbours

        # military #
        self.troops_stationed = 0
    
    ### SETTERS ###
    
    def setID(self, id: str) -> None:
        self.id = id

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

    def getName(self) -> str:
        return self.name
    
    def getID(self) -> str:
        return self.id

    def getRuler(self) -> Player:
        return self.ruler
    
    def getTroops(self) -> int:
        return self.troops_stationed
    
    ### ACTIONS ###

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.circle(screen, Color(self.ruler.color), (self.x, self.y), TERRITORY_MARKER_RADIUS)

    def isEmpty(self) -> bool:
        return self.ruler is None


class Continent:

    def __init__(self, name: str, territories: dict[str: Territory], bonus_troops: int) -> None:

        # geography #
        self.name: str = name
        self.territories: dict[str: Territory] = territories
        
        self.territories_list: list[Territory] = []
        for territory in self.territories.values():
            self.territories_list.append(territory)

        self.ruler: Player = None

        # military #
        self.bonus_troops: int = bonus_troops
    
    ### SETTERS ###
    
    def setRuler(self, new_ruler: Player) -> None:
        self.ruler = new_ruler
    
    def setBonusTroops(self, bonus_troops: int) -> None:
        self.bonus_troops = bonus_troops
    
    ### GETTERS ###

    def getName(self) -> str:
        return self.name

    def getTerritories(self) -> dict[str: Territory]:
        return self.territories

    def getTerritoriesList(self) -> list[Territory]:
        return self.territories_list

    def getRuler(self) -> Player:
        return self.ruler
    
    def getBonusTroops(self) -> int:
        return self.bonus_troops

    ### ACTIONS ###

    def drawTerritories(self, screen: pg.Surface):
        for territory in self.getTerritoriesList():
            territory.draw(screen)

    def findTerritory(self, territory_id: str) -> Territory:
        if territory_id in self.territories.keys():
            return self.territories[territory_id]
        return None
    
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
    
    def getRuler(self) -> Player:
        if self.hasSingleRuler():
            return self.territories_list[0].ruler
        return None

class Game:

    def __init__(self, continents: dict[str: Continent]) -> None:
        
        # players #
        self.players: list[Player] = []
        self.active_player: Player

        # dice #
        self.dice: list[list[int]] = [[0, 0], [0, 0, 0]]

        # map #
        self.continents: dict[str: Continent] = continents
        self.continents_list: list[Continent] = []

        for continent in self.continents.values():
            self.continents_list.append(continent)
        
        # game #
        self.phase: int = 0
        self.first_territory: Territory = None      # territory from which an attack will be launched

        # init #
        self.create_players()
        self.assignTerritories()
        self.passPhase()
    
    ### SETTERS ###

    def setFirstTerritory(self, territory: Territory) -> None:
        self.first_territory = territory

        if self.phase == 2:
            print(f"attacking from {self.first_territory.name}")
        elif self.phase == 3:
            print(f"moving troops from {self.first_territory.name}")
    
    def rollDice(self) -> None:
        for role in range(len(self.dice)):
            for dice in range(len(self.dice[role])):
                self.dice[role][dice] = random.randint(1, 6)
            self.dice[role].sort()
        

    ### GETTERS ###

    def getPlayers(self) -> list[Player]:
        return self.players

    def getContinents(self) -> dict[str: Continent]:
        return self.continents
    
    def getContinentsList(self) -> list[Continent]:        
        return self.continents_list
    
    def hasSelectedFirstTerritory(self) -> bool:
        return self.first_territory is not None

    ### ACTIONS ###

    # --- players --- #
    
    def create_players(self) -> None:
        # n_players: int = int(input("enter the number of players: "))
        n_players: int = 6
        colors: list[str]= ["red", "green", "blue", "black", "orange", "purple"]
        color: str
        color_taken: bool = False

        for i in range(n_players):

            # choose player color #
            # color = input(f"enter player {i+1}'s color: ")

            color = colors[i]
            
            for player in self.players:
                if player.color == color:
                    color_taken = True
            
            while color_taken:
                color_taken = False
                color = input("color taken, choose a different one: ")
                for player in self.players:
                    if player.color == color:
                        color_taken = True
            
            self.players.append(Player(color))
        
        self.active_player = self.players[0]

    def passTurn(self) -> None:
        player_turn: int = self.players.index(self.active_player)
        player_turn += 1
        if player_turn == len(self.players):
            player_turn = 0
        self.active_player = self.players[player_turn]
        
        # add drafting troops #
        self.active_player.setTroops(self.calculateDraftTroops(self.active_player))

        if not self.phase == 0:     # don't print during the setup phase
            print(f"it is now {self.active_player.color}'s turn")
    
    def countPlayerTerritories(self, player: Player) -> int:

        count: int = 0

        for continent in self.getContinentsList():
            for territory in continent.getTerritoriesList():
                if territory.ruler == player:
                    count += 1
        
        return count

    def calculateDraftTroops(self, player: Player) -> int:
        draft_troops: int = 3   # by default, player gets 3 troops

        # bonus troops for ruling entire continents >>>
        for continent in self.continents_list:
            if continent.getRuler() == player:
                draft_troops += continent.bonus_troops
        # <<<

        return draft_troops

    # --- map --- #

    def assignTerritories(self) -> None:
        
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
            
            # assisng territory
            chosen_territory.ruler = self.active_player      # assign ruler
            chosen_territory.addTroops(1)       # every territory needs to have at least 1 troop

            # check if there are any territories left
            empty_territories_left = True
            for continent in self.getContinentsList():
                if continent.hasEmptyTerritories():
                    empty_territories_left = False
            
            assigning_territories = not empty_territories_left
            self.passTurn()

    def drawTerritories(self, screen: pg.Surface) -> None:
        for continent in self.continents_list:
            continent.drawTerritories(screen)

    def findTerritory(self, territory_id: str) -> Territory:
        territory: Territory = None
        for continent in self.getContinentsList():
            if territory is None:
                territory = continent.findTerritory(territory_id)
        
        return territory

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
        
        return None

    # --- game --- #

    def passPhase(self) -> None:
        
        if self.phase == 2 or self.phase == 3:      # at the end of attack and fortify phases: reset
            self.first_territory = None
        
        self.phase += 1
        if self.phase == 4:     # there are only 3 phases: draft, attack, fortify
            self.phase = 1
            self.passTurn()     # at the end of phase 3, it is the next player's turn
        
        print(f"phase: {self.phase}")
    
    def conquerTerritory(self, territory_conquered_id: str, conqueror: Player, occupying_force: int) -> None:
        territory_conquered: Territory = self.findTerritory(territory_conquered_id)
        territory_conquered.setRuler(conqueror)
        territory_conquered.setTroops(occupying_force)
        print(f"{territory_conquered.name} was conquered by {conqueror.color}")

    def attack(self, defending_territory: Territory) -> None:

        attacking_troops: int
        defending_troops: int

        while defending_territory.getTroops() > 0 and self.first_territory.getTroops() > 1:
            
            attacking_troops = self.first_territory.getTroops()
            defending_troops = defending_territory.getTroops()

            self.rollDice()

            # number of battles depends on lowest number of troops >>>
            for battle in range(min(defending_troops, attacking_troops - 1)):
                if self.dice[0][battle] >= self.dice[1][battle]:   # defence wins battle
                    self.first_territory.removeTroop()
                else:
                    defending_territory.removeTroop()
            
            print(f"{self.first_territory.name} lost: {attacking_troops - self.first_territory.getTroops()}")
            print(f"{defending_territory.name} lost: {defending_troops - defending_territory.getTroops()}")
            print(f"battle: {self.first_territory.name} {self.first_territory.getTroops()} | {defending_territory.getTroops()} {defending_territory.name}")
            print()
        
        if defending_territory.getTroops() == 0:
            self.conquerTerritory(defending_territory.getID(), self.active_player, self.first_territory.getTroops())