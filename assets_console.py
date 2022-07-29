def addSpace() -> None:
    for _ in range(5):
        print()


class Player:

    def __init__(self, player_color: str = "n/a") -> None:

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

    def __init__(self, name: str, neighbours: list[str] = []) -> None:

        # geography #
        self.name: str = name
        self.ruler = None
        self.neighbours: list[str] = neighbours

        # military #
        self.troops_stationed = 0
    
    ### SETTERS ###
    
    def setRuler(self, new_ruler: Player) -> None:
        self.ruler = new_ruler
    
    def setTroops(self, number_troops: int) -> None:
        self.troops_stationed = number_troops

    def addTroops(self, number_troops: int) -> None:
        self.troops_stationed += number_troops
    
    def removeTroops(self, number_troops: int) -> None:
        self.troops_stationed -= number_troops
    
    ### GETTERS ###

    def getName(self) -> str:
        return self.name
    
    def getRuler(self) -> Player:
        return self.ruler
    
    def getTroops(self) -> int:
        return self.troops_stationed
    
    ### ACTIONS ###

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

    def findTerritory(self, territory_id: str) -> Territory:
        return self.territories[territory_id]
    
    def hasEmptyTerritories(self) -> bool:
        for territory in self.getTerritoriesList():
            if territory.isEmpty():
                return True
        return False


class Game:

    def __init__(self, continents: dict[str: Continent]) -> None:
        
        # players
        self.players: list[Player] = []
        self.create_players()
        self.active_player: Player

        # map #
        self.continents: dict[str: Continent] = continents
        self.continents_list: list[Continent] = []

        for continent in self.continents.values():
            self.continents_list.append(continent)
        
        # game #
        self.phase: int = 0
    
    ### GETTERS ###

    def getPlayers(self) -> list[Player]:
        return self.players

    def getContinents(self) -> dict[str: Continent]:
        return self.continents
    
    def getContinentsList(self) -> list[Continent]:        
        return self.continents_list
    
    ### ACTIONS ###

    # --- players --- #
    
    def create_players(self) -> None:
        
        addSpace()

        n_players: int = int(input("enter the number of players: "))
        color: str
        color_taken: bool = False

        for i in range(n_players):

            # choose player color #
            color = input(f"enter player {i+1}'s color: ")
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
        print(f"it is now {self.active_player}'s turn")
    
    def countPlayerTerritories(self, player: Player) -> int:

        count: int = 0

        for continent in self.getContinentsList():
            for territory in continent.getTerritoriesList():
                if territory.ruler == player:
                    count += 1
        
        return count

    # --- map --- #

    def findTerritory(self, territory_id: str) -> Territory:
        territory: Territory = None
        for continent in self.getContinentsList():
            if territory is None:
                territory = continent.findTerritory(territory_id)
        
        return territory

    # --- game --- #

    def passPhase(self) -> None:
        
        self.phase += 1
        if self.phase == 4:
            self.phase = 1
            self.passTurn()