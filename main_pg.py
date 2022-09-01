import pygame as pg
from constants import *
from pygame.locals import *
from assets_pg import *
from maps.classic_pg import *
from math import sqrt


### ----- VARIABLES ------ ###


game: Game = Game(CLASSIC_MAP, classic_continents)

selected_territory: Territory = NULL_TERRITORY

# --- HUD --- #

# fonts #
phase_font: pg.font.Font    # "DRAFT", "ATTACK" or "FORTIFY"
territory_card_font: pg.font.Font       # first territory card's design
cards_exit_button_font: pg.font.Font    # X on exit button
trade_button_font: pg.font.Font     # "TRADE" on trade button

# territory cards view #
cards_selected: list[TerritoryCard] = [NULL_TERRITORY_CARD for i in range(3)]

# --- pygame --- #

pg.init()
screen: pg.Surface = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("'we have RISK at home' - RISK at home:")
cards_view_screen: pg.Surface = pg.Surface((CARDS_VIEW_WIDTH, CARDS_VIEW_HEIGHT))

clock: pg.time.Clock = pg.time.Clock()

running: bool = True


### ------ FUNCTIONS ------ ###


# --- UI --- #

def drawPlayerIcons(players: list[Player], active_player: Player, outline_width = 3) -> None:
    
    """
    1 -> WIDTH//2
    2 -> WIDTH//2 - GAP//2 - RADIUS
    3 -> WIDTH//2 - GAP - 2 * RADIUS
    ...
    """

    player_icon_x_0: int = WIDTH//2 - (len(players) - 1) * PLAYER_ICON_GAP//2 - (len(players) - 1) * PLAYER_ICON_RADIUS    # math
    
    backplate_x: int = player_icon_x_0 - (2 * PLAYER_ICON_RADIUS)
    backplate_y: int = -WIDTH//50
    backplate_width: int = (len(players) - 1) * PLAYER_ICON_GAP + (len(players) + 1) * (2 * PLAYER_ICON_RADIUS)
    backplate_height: int = int(2.8 * PLAYER_ICON_HEIGHT)
    
    # backplate #
    pg.draw.rect(screen, Color(PLAYER_ICONS_BACKPLATE_COLOR), (backplate_x, backplate_y, backplate_width, backplate_height), 0, PLAYER_ICONS_BACKPLATE_ROUND_CORNER)
    
    # player icons #
    for player_index, player in enumerate(players):
        
        player_icon_x: int = player_icon_x_0 + (player_index * PLAYER_ICON_GAP) + (player_index * (2 * PLAYER_ICON_RADIUS))    # math
        player_icon_y: int = PLAYER_ICON_HEIGHT
        outline_color: list[int, int, int] = [Color(player.getColor()).r, Color(player.getColor()).g, Color(player.getColor()).b]      # extract original values
        for i in range(3):
            outline_color[i] //= 2      # make outline darker
        
        # active player icon is drawn slightly below the rest to make it stand out
        if player == active_player:
            player_icon_y += PLAYER_ICON_RADIUS//2

        pg.draw.circle(screen, Color(player.getColor()), (player_icon_x, player_icon_y), PLAYER_ICON_RADIUS)    # background
        pg.draw.circle(screen, Color(outline_color[0], outline_color[1], outline_color[2]), (player_icon_x, player_icon_y), PLAYER_ICON_RADIUS, outline_width)      # outline


def drawGamePhaseIcons(current_phase: int, outline_width = 2, round_corners = 3) -> None:
    
    """
    DRAFT -> HEIGHT//2 - GAP - 3 * LENGTH//2
    ATTACK -> HEIGHT//2 - LENGTH//2
    FORTIFY -> HEIGHT//2 + GAP + LENGTH//2
    """
    
    y_0 = HEIGHT//2 - PHASE_ICON_GAP - 3 * PHASE_ICON_LENGTH//2
    
    for i in range(3):
        
        # card #
        width: int = PHASE_ICON_LENGTH
        if i == current_phase:
            width = ACTIVE_PHASE_ICON_WIDTH
        
        x: int = WIDTH - width
        y: int = y_0 + (i * PHASE_ICON_GAP) + (i * PHASE_ICON_LENGTH)
        
        pg.draw.rect(screen, Color(CARD_BG_COLOR), (x, y, width, PHASE_ICON_LENGTH), 0, round_corners)    # background
        pg.draw.rect(screen, Color(CARD_COLOR), (x, y, width, PHASE_ICON_LENGTH), outline_width, round_corners)  # outline
        
        # text #
        font = pg.font.Font(None, PHASE_ICON_TEXT_SIZE)
        text = font.render(PHASE_NAMES[i][0].upper(), True, CARD_COLOR)
        text_rect = text.get_rect(center = (x + width//2, y + PHASE_ICON_LENGTH//2))
        screen.blit(text, text_rect)


def drawGamePhaseInfo(text_str: str, active_player_color: str, outline_width: int = 2, round_corners: int = 3) -> None:
    
    # text #
    font: pg.font.Font = pg.font.Font(None, FONT_SIZE)
    text = font.render(text_str, True, active_player_color)
    text_rect = text.get_rect(center = (int(1.2 * ACTIVE_PLAYER_BAND_OUTLINE) + PHASE_ICON_LENGTH//2, HEIGHT//2))
    
    # background rect #
    bg_color: str = TEXT_BG_COLOR
    outline_color: str = active_player_color
    if active_player_color in DARK_COLORS:
        bg_color = TEXT_COLOR
    
    x: int = text_rect.x - text_rect.width//4
    y: int = text_rect.y - text_rect.height//4
    width: int = 3 * text_rect.width//2
    height: int = 3 * text_rect.height//2
    
    # blit #
    pg.draw.rect(screen, Color(bg_color), (x, y, width, height), 0, round_corners)    # background
    pg.draw.rect(screen, Color(outline_color), (x, y, width, height), outline_width, round_corners)  # background
    screen.blit(text, text_rect)


def displaySelectedTerritoryName(territory: Territory, outline_width: int = 2, round_corners: int = 3) -> None:
    
    # text #
    font: pg.font.Font = pg.font.Font(None, FONT_SIZE)
    text = font.render(selected_territory.getName(), True, Color(selected_territory.getRuler().getColor()))
    text_rect = text.get_rect(center = (WIDTH//2, SELECTED_TERRITORY_NAME_HEIGHT))
    
    # background rect #
    bg_color: str = TEXT_BG_COLOR
    outline_color: str = territory.getRuler().getColor()
    if territory.getRuler().getColor() in DARK_COLORS:
        bg_color = TEXT_COLOR

    x: int = text_rect.x - int(0.05 * text_rect.width)
    y: int = text_rect.y - int(0.2 * text_rect.height)
    width: int = int(1.1 * text_rect.width)
    height: int = int(1.4 * text_rect.height)
    
    # blit #
    pg.draw.rect(screen, Color(bg_color), (x, y, width, height), 0, round_corners)  # background
    pg.draw.rect(screen, Color(outline_color), (x, y, width, height), outline_width, round_corners)  # background
    screen.blit(text, text_rect)


# --- map --- #

# recursively determine whether 2 territories are connected by checking if the neighbours of T2, with ruler equal to T2's ruler, are connected to T1
def areConnected(territory1: Territory, territory2: Territory, territories_traversed: list[Territory] | None = None) -> bool:
    
    if territories_traversed is None:
        territories_traversed = [territory2]
    elif len(territories_traversed) > game.countTerritories():      # if more territories have been visited than there are in the map, something went wrong
        raise Exception(f"recursion depth too long: trying to find connection from {territory2.getName()} to {territory1.getName()}")
    
    # territories owned by different players are never connected
    if territory1.getRuler().getColor() != territory2.getRuler().getColor():
        return False
        
    # 2 neighbour territories owned by the same player are always connected
    if territory1.getID() in territory2.getNeighbours():
        return True
    
    # if T1 and T2 are not neighbours, check if any of T2's neighbours are connected to T1, in which case T2 is also connected to T1
    for t2_neighbour in territory2.getNeighbours():
        
        t2_neighbour_territory: Territory = game.findTerritory(t2_neighbour)
        
        # check only neighbour territories that are owned by the same player and have not yet been traversed (avoid infinite loops)
        if t2_neighbour_territory.getRuler().getColor() == territory1.getRuler().getColor() and t2_neighbour_territory not in territories_traversed:
            
            t1_continent: Continent = game.findTerritoryContinent(territory1.getID())
            t2_continent: Continent = game.findTerritoryContinent(territory2.getID())
            neighbour_continent: Continent = game.findTerritoryContinent(t2_neighbour_territory.getID())

            # optimization: if T1 and T2 belong to the same continent, stay in that continent >
            if not (t1_continent == t2_continent and neighbour_continent != t1_continent):
                territories_traversed.append(t2_neighbour_territory)
                if areConnected(territory1, t2_neighbour_territory, territories_traversed):
                    return True
    
    # remove T2 as it didn't contribute
    if territory2 in territories_traversed:
        territories_traversed.remove(territory2)
    return False


# mark a given territory with a square of a given color
def squareMark(territory: Territory, mark_color: str) -> None:
    pg.draw.rect(screen, Color(mark_color), (territory.x - TERRITORY_MARKER_RADIUS, territory.y - TERRITORY_MARKER_RADIUS,
                 TERRITORY_MARKER_RADIUS*2, TERRITORY_MARKER_RADIUS*2), 3)


def triangleMark(territory: Territory, mark_color: str) -> None:
    sw_point: tuple[int, int] = (territory.x - ATTACKER_MARKER_SIDE_LENGTH // 2, territory.y + TERRITORY_MARKER_RADIUS)  # math
    se_point: tuple[int, int] = (territory.x + ATTACKER_MARKER_SIDE_LENGTH // 2, sw_point[1])  # math
    n_point: tuple[int, int] = (territory.x, territory.y - (int(sqrt(3) * ATTACKER_MARKER_SIDE_LENGTH / 2) - TERRITORY_MARKER_RADIUS))
    
    pg.draw.line(screen, Color(mark_color), sw_point, se_point, 3)
    pg.draw.line(screen, Color(mark_color), sw_point, n_point, 3)
    pg.draw.line(screen, Color(mark_color), n_point, se_point, 3)


def euclidianDistance(a: tuple[int, int], b: tuple[int, int]) -> float:
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


# --- territory cards --- #

def drawSelectedCards(outline_width: int = 3, round_corners: int = 2) -> None:
    
    for i in range(len(cards_selected)):
        
        # determine colors >>>
        card_bg_color: str = PLAYER_CARD_BG_COLOR
        card_outline_color: str = PLAYER_CARD_OUTLINE_COLOR
        if cards_selected[i].isNull():
            card_bg_color = SELECTED_SLOT_BG_COLOR
            card_outline_color = SELECTED_SLOT_COLOR
        # <<<
        
        pg.draw.rect(screen, Color(card_bg_color), (SELECTED_SLOT_X_COORDS[i], SELECTED_SLOT_Y, SELECTED_SLOT_WIDTH, SELECTED_SLOT_HEIGHT), 0, round_corners)
        pg.draw.rect(screen, Color(card_outline_color), (SELECTED_SLOT_X_COORDS[i], SELECTED_SLOT_Y, SELECTED_SLOT_WIDTH, SELECTED_SLOT_HEIGHT), outline_width, round_corners)
        
        if not cards_selected[i].isNull():
            # card design text >>>
            font: pg.font.Font = pg.font.Font(None, 2 * FONT_SIZE)
            text = font.render(cards_selected[i].design.upper(), True, PLAYER_CARD_TEXT_COLOR)  # first letter of card type
            text_rect = text.get_rect(center = (SELECTED_SLOT_X_COORDS[i] + SELECTED_SLOT_WIDTH//2, SELECTED_SLOT_Y + SELECTED_SLOT_HEIGHT//2))
            screen.blit(text, text_rect)
            # <<<


def calculatePlayerCardsXCoordinates(n_cards: int) -> list[int]:
    
    if n_cards == 0:
        return []
    
    gap: int = PLAYER_CARD_WIDTH//n_cards   # gap between each card
    first_x: int = WIDTH//2 - (n_cards - 1) * gap//2 - n_cards * PLAYER_CARD_WIDTH//2     # math
    
    return [first_x + (i * gap) + (i * PLAYER_CARD_WIDTH) for i in range(n_cards)]      # math
    

def drawPlayerCards(outline_width: int = 3, round_corners: int = 2) -> None:
    
    n_cards: int = len(game.active_player.getTerritoryCards())
    x_coords: list[int] = calculatePlayerCardsXCoordinates(n_cards)
    
    for i in range(n_cards):
        
        # card background >
        pg.draw.rect(screen, Color(PLAYER_CARD_BG_COLOR), (x_coords[i], PLAYER_CARD_Y, PLAYER_CARD_WIDTH, PLAYER_CARD_HEIGHT), 0, round_corners)
        
        # card outline >
        pg.draw.rect(screen, Color(PLAYER_CARD_OUTLINE_COLOR), (x_coords[i], PLAYER_CARD_Y, PLAYER_CARD_WIDTH, PLAYER_CARD_HEIGHT), outline_width, round_corners)
        
        # card design text >>>
        font: pg.font.Font = pg.font.Font(None, 2 * FONT_SIZE)
        text = font.render(game.active_player.getTerritoryCards()[i].design.upper(), True, PLAYER_CARD_TEXT_COLOR)      # first letter of card type
        text_rect = text.get_rect(center = (x_coords[i] + PLAYER_CARD_WIDTH//2, PLAYER_CARD_Y + PLAYER_CARD_HEIGHT//2))
        screen.blit(text, text_rect)
        # <<<


def selectPlayerCard(click_coords: tuple[int, int]) -> TerritoryCard:
    
    # check if y-coords match
    if PLAYER_CARD_Y <= click_coords[1] <= PLAYER_CARD_Y + PLAYER_CARD_HEIGHT:
        # check if x-coords match for any available card
        x_coords: list[int] = calculatePlayerCardsXCoordinates(len(game.active_player.getTerritoryCards()))
        for i, x in enumerate(x_coords):
            if x <= click_coords[0] <= x + PLAYER_CARD_WIDTH:
                return game.active_player.getTerritoryCards()[i]    # x_coords are calculated in same order as player's cards list
        
        return NULL_TERRITORY_CARD
    return NULL_TERRITORY_CARD


# look for the first empty slot and place it (if available)
def placeSelectedCard(card_to_be_placed: TerritoryCard) -> None:
    global cards_selected
    card_placed: bool = False
    for i in range(len(cards_selected)):
        if cards_selected[i].isNull() and not card_placed:  # make sure card hasn't already been placed
            cards_selected[i] = card_to_be_placed
            game.active_player.removeTerritoryCard(card_to_be_placed)
            card_placed = True


def deselectPlayerCard(click_coords: tuple[int, int]) -> TerritoryCard:
    
    # check if y-coords match
    if SELECTED_SLOT_Y <= click_coords[1] <= SELECTED_SLOT_Y + SELECTED_SLOT_HEIGHT:
        # check if x-coords match for any available card
        for i, x in enumerate(SELECTED_SLOT_X_COORDS):
            if x <= click_coords[0] <= x + SELECTED_SLOT_WIDTH:
                return cards_selected[i]
        
        return NULL_TERRITORY_CARD
    return NULL_TERRITORY_CARD


def getSetOfTerritoryCards(given_design: str, cards: list[TerritoryCard]) -> list[TerritoryCard]:
    
    cards_copy: list[TerritoryCard] = cards[:]
    cards_set: list[TerritoryCard] = []     # return value
    
    # one specific design (infantry, cavalry or artillery) #
    if given_design != 'm':
        for territory_card in cards_copy[:]:
            if territory_card.design == given_design or territory_card.design == WILD_CARD.design:
                cards_set.append(territory_card)
                cards_copy.remove(territory_card)       # remove card from 'cards_copy' to avoid duplicates
                if len(cards_set) == 3:     # if 'cards_set' contains 3 cards, set is complete
                    return cards_set
        
        return []
    
    # one of each #
    for design in [INFANTRY_CARD.design, CAVALRY_CARD.design, ARTILLERY_CARD.design]:
        design_found: bool = False  # speed up process
        # first look for a non-wildcard match >>>
        for territory_card in cards_copy[:]:
            if not design_found and territory_card.design == design:
                cards_set.append(territory_card)
                cards_copy.remove(territory_card)
                design_found = True
                if len(cards_set) == 3:
                    return cards_set
        # <<<
        
        # otherwise use a wildcard (if available) >>>
        if not design_found:    # optimization: don't go into the loop unless necessary
            for territory_card in cards_copy[:]:
                if not design_found and territory_card.design == WILD_CARD.design:
                    cards_set.append(territory_card)
                    cards_copy.remove(territory_card)
                    design_found = True
                    if len(cards_set) == 3:
                        return cards_set
        # <<<
    
    return []


def hasSetOfTerritoryCards(cards: list[TerritoryCard]) -> bool:
    
    for design in ['m', INFANTRY_CARD.design, CAVALRY_CARD.design, ARTILLERY_CARD.design]:
        if len(getSetOfTerritoryCards(design, cards)) == 3:
            return True
    
    return False


### ------ CLASSES ------ ###


### ------ MAIN ------ ###


while running:
    
    # EVENTS #

    for event in pg.event.get():

        if event.type == QUIT:
            running = False
        
        elif event.type == KEYUP:

            if event.key == K_ESCAPE:
                running = False
            
            if event.key == K_RETURN or event.key == K_SPACE:
                # can't skip DRAFT phase before drafting all troops or if holding more than 5 territory cards >
                if game.phase != 1 or (game.active_player.getTroops() == 0 and game.phase == 1 and len(game.active_player.getTerritoryCards()) < 5):
                    game.passPhase()
                    selected_territory = NULL_TERRITORY     # reset UI
        
        elif event.type == MOUSEBUTTONUP:
            
            click: tuple[int, int] = pg.mouse.get_pos()
            
            if not game.isViewingTerritoryCards():      # in map view
                # check if clicked on territory cards window button
                if TERRITORY_CARD_COORDS[0] <= click[0] <= TERRITORY_CARD_COORDS[0] + CARD_WIDTH \
                   and TERRITORY_CARD_COORDS[1] <= click[1] <= TERRITORY_CARD_COORDS[1] + CARD_HEIGHT and len(game.active_player.getTerritoryCards()) > 0:
                    game.toggleTerritoryCardsWindow()
                
                else:   # normal game actions
                    selected_territory = game.selectTerritory(click)
        
                    if game.phase == 1 and not selected_territory.isNull():     # draft phase
                        game.setFirstTerritory(selected_territory)
                        if game.first_territory.ruler == game.active_player and not game.active_player.getTroops() == 0:      # selected a valid territory
                            game.draftTroops()
                            
                            # check if draft phase is over (no more troops and no available territory card sets -> auto pass phase / player was in overflow of territory
                            # cards -> go back to ATTACK phase as soon as this is no longer the case)
                            if game.active_player.available_troops == 0 and (not hasSetOfTerritoryCards(game.active_player.getTerritoryCards()) or
                                                                             game.hasTerritoryCardOverflow()):
                                game.passPhase()
                                if game.hasTerritoryCardOverflow():
                                    game.toggleTerritoryCardsOverflow()
                    
                    elif game.phase == 2:     # attack phase
                        
                        # set attacking territory
                        if selected_territory.ruler == game.active_player or selected_territory.isNull():
                            game.setFirstTerritory(selected_territory)
                        
                        # begin attack
                        elif game.hasSelectedFirstTerritory() and selected_territory.getID() in game.first_territory.getNeighbours() and \
                                selected_territory.ruler != game.first_territory.ruler:
                            
                            game.attack(selected_territory)
                            
                            # update screen so player can see how many troops they can work with >>>
                            game.drawTerritories(screen)
                            pg.display.update()
                            time.sleep(0.1)     # pg needs a bit of time to update screen
                            # <<<
                            
                            if selected_territory.getTroops() == 0:     # attack successful
                                
                                # end game >>>
                                if len(game.players) == 2 and len(game.getPlayerTerritories(selected_territory.getRuler())) == 1:
                                    running = False
                                    print(f"\ngame over, {game.active_player.color.upper()} wins through world conquest!")
                                # <<<
                                
                                else:
                                    game.advanceTroops(selected_territory)
                                    if not game.playerHasReceivedCard():
                                        game.receiveCard()
                            
                            else:  # attack failed
                                print(f"{selected_territory.name} defended fiercely and annihilated {game.first_territory.name}'s "
                                      f"attacking force")
                            
                    elif game.phase == 3:   # fortify phase
                        if selected_territory.isNull():
                            game.setFirstTerritory(NULL_TERRITORY)
                        elif selected_territory.ruler == game.active_player:
                            if game.hasSelectedFirstTerritory() and game.first_territory != selected_territory and areConnected(game.first_territory, selected_territory) \
                                    and game.first_territory.getTroops() > 1:
                                game.fortify(selected_territory)
                            else:
                                game.setFirstTerritory(selected_territory)
                        else:
                            game.setFirstTerritory(NULL_TERRITORY)
            
            else:   # in territory cards view
                
                # check if clicked exit button
                if euclidianDistance(click, CARDS_EXIT_COORDS) <= CARDS_EXIT_RADIUS:
                    
                    for card in cards_selected:
                        if not card.isNull():
                            game.active_player.addTerritoryCard(card)       # return all unused cards to player
                    cards_selected = [NULL_TERRITORY_CARD for i in range(3)]    # reset 'cards_selected'
                    
                    game.toggleTerritoryCardsWindow()     # exit territory cards window
                
                # check if clicked on trade button
                elif TRADE_BUTTON_COORDS[0] <= click[0] <= (TRADE_BUTTON_COORDS[0] + TRADE_BUTTON_WIDTH) and \
                        TRADE_BUTTON_COORDS[1] <= click[1] <= (TRADE_BUTTON_COORDS[1] + TRADE_BUTTON_HEIGHT):
                    
                    # check that player has selected 3 territory cards
                    if not cards_selected[0].isNull() and not cards_selected[1].isNull() and not cards_selected[2].isNull():
                        
                        # trade in cards
                        if hasSetOfTerritoryCards(cards_selected):
                            game.trade_troops()
                            cards_selected = [NULL_TERRITORY_CARD for i in range(3)]    # reset 'cards_selected'
                            game.toggleTerritoryCardsWindow()       # exit territory cards view window
                
                elif game.phase == 1:
                    
                    # check if clicked a player's territory card
                    selected_card: TerritoryCard = selectPlayerCard(click)
                    if not selected_card.isNull():      # clicked on a card
                        placeSelectedCard(selected_card)    # place card on empty slots
                    
                    # check if deselected a territory card >>>
                    else:
                        deselected_card: TerritoryCard = deselectPlayerCard(click)
                        if not deselected_card.isNull():    # clicked on a card
                            index: int = cards_selected.index(deselected_card)      # index of 'deselected_card' in 'cards_selected'
                            # return card to player
                            cards_selected[index] = NULL_TERRITORY_CARD     # reset
                            # push selected cards to the left >>>
                            while index < len(cards_selected) - 1:
                                cards_selected[index], cards_selected[index + 1] = cards_selected[index + 1], cards_selected[index]
                                index += 1
                            # <<<
                            game.active_player.addTerritoryCard(deselected_card)    # return card

    # GAME #
    
    # REFRESH #

    screen.fill(BG_COLOR)
    
    if game.isViewingTerritoryCards():
        # fade out background #
        game.map.set_alpha(100)
        screen.blit(game.map, (0, 0))
        
        # exit button #
        pg.draw.circle(screen, Color(CARDS_EXIT_BG_COLOR), CARDS_EXIT_COORDS, CARDS_EXIT_RADIUS)    # bg
        pg.draw.circle(screen, Color(CARDS_EXIT_OUTLINE_COLOR), CARDS_EXIT_COORDS, CARDS_EXIT_RADIUS, CARDS_EXIT_OUTLINE_WIDTH)  # outline
        
        cards_exit_button_font = pg.font.Font(None, FONT_SIZE)
        cards_exit_button_text = cards_exit_button_font.render("X", True, "black")      # text
        cards_exit_button_text_rect = cards_exit_button_text.get_rect(center = CARDS_EXIT_COORDS)       # text position
        screen.blit(cards_exit_button_text, cards_exit_button_text_rect)    # blit text
        
        # trade button #
        pg.draw.rect(screen, Color(TRADE_BUTTON_BG_COLOR), (TRADE_BUTTON_COORDS[0], TRADE_BUTTON_COORDS[1], TRADE_BUTTON_WIDTH, TRADE_BUTTON_HEIGHT), 0, 4)     # bg
        pg.draw.rect(screen, Color(TRADE_BUTTON_OUTLINE_COLOR), (TRADE_BUTTON_COORDS[0], TRADE_BUTTON_COORDS[1], TRADE_BUTTON_WIDTH, TRADE_BUTTON_HEIGHT), 3, 4)  # outline
        
        trade_button_font = pg.font.Font(None, FONT_SIZE)
        trade_button_text = trade_button_font.render("TRADE", True, TRADE_BUTTON_TEXT_COLOR)    # text
        trade_button_text_rect = trade_button_text.get_rect(center = TRADE_BUTTON_CENTER)       # text position
        screen.blit(trade_button_text, trade_button_text_rect)      # blit text
        
        # display selected territory cards #
        drawSelectedCards()
        
        # display player's territory cards #
        drawPlayerCards()
    else:
        game.map.set_alpha(255)
        screen.blit(game.map, (0, 0))
        game.drawTerritories(screen)
    
        # --- UI --- #
        
        # players #
        drawPlayerIcons(game.players, game.active_player)
        
        # current phase #
        drawGamePhaseIcons(game.phase - 1)
    
        # draft phase #
        if game.phase == 1:
            drawGamePhaseInfo(f"+{game.active_player.getTroops()}", game.active_player.getColor())
        
        # possible attacks markers #
        # draw a square around all territories that can be attacked
        if game.phase == 2:
            if game.hasSelectedFirstTerritory() and game.first_territory.troops_stationed > 1:  # mark only neighbouring territories to 'game.first_territory'
                for neighbour in game.first_territory.neighbours:
                    neighbour_territory: Territory = game.findTerritory(neighbour)
                    if neighbour_territory.ruler != game.active_player:
                        squareMark(neighbour_territory, game.active_player.color)
            else:
                for player_territory in game.getPlayerTerritories(game.active_player):      # list all territories owned by the active player
                    if player_territory.troops_stationed > 1:   # can't attack with only 1 troop stationed
                        for neighbour in player_territory.getNeighbours():
                            neighbour_territory: Territory = game.findTerritory(neighbour)
                            if neighbour_territory.ruler != game.active_player:
                                squareMark(neighbour_territory, game.active_player.color)
        
        # attacker / fortify origin marker #
        if game.phase >= 2 and game.hasSelectedFirstTerritory():
            triangleMark(game.first_territory, game.active_player.color)
        
        # mark possible origins / destinations during fortify phase #
        if game.phase == 3:
            # origins
            if not game.hasSelectedFirstTerritory():
                for player_territory in game.getPlayerTerritories(game.active_player):
                    if player_territory.troops_stationed > 1:   # need at least 2 troops stationed to fortify
                        # filter only territories which have at least 1 friendly neighbour >>>
                        has_friendly_neighbour: bool = False
                        i: int = 0
                        while not has_friendly_neighbour and i < len(player_territory.neighbours):
                            if game.findTerritory(player_territory.neighbours[i]).ruler.color == game.active_player.color:
                                has_friendly_neighbour = True
                            i += 1
                        # <<<
                        if has_friendly_neighbour:
                            triangleMark(player_territory, game.active_player.color)
                        
            # destinations
            elif game.first_territory.troops_stationed > 1:
                for player_territory in game.getPlayerTerritories(game.active_player):
                    if player_territory != game.first_territory and areConnected(game.first_territory, player_territory):
                        squareMark(player_territory, game.active_player.color)
        
        # selected territory's name #
        if not selected_territory.isNull():
            displaySelectedTerritoryName(selected_territory)
        
        # territory cards #
        if len(game.active_player.getTerritoryCards()) > 0:
            pg.draw.rect(screen, Color(CARD_BG_COLOR), (TERRITORY_CARD_COORDS[0], TERRITORY_CARD_COORDS[1], CARD_WIDTH, CARD_HEIGHT), 0, 2)     # clean bg
            pg.draw.rect(screen, Color(CARD_COLOR), (TERRITORY_CARD_COORDS[0], TERRITORY_CARD_COORDS[1], CARD_WIDTH, CARD_HEIGHT), 3, 2)    # outline
            territory_card_font = pg.font.Font(None, CARD_FONT_SIZE)
            territory_card_text = territory_card_font.render("T", True, Color(CARD_COLOR))
            territory_card_text_rect = territory_card_text.get_rect(center = (TERRITORY_CARD_COORDS[0] + CARD_WIDTH//2, TERRITORY_CARD_COORDS[1] + 2*CARD_HEIGHT//3))
            screen.blit(territory_card_text, territory_card_text_rect)

    # player turn #
    # colored box on top-left corner
    # if game.active_player.color != "black":
    #     pg.draw.rect(screen, Color("black"), (2, 2, 60, 30), 5)
    # else:
    #     pg.draw.rect(screen, Color("white"), (2, 2, 60, 30), 5)
    # pg.draw.rect(screen, Color(game.active_player.color), (2, 2, 60, 30))

    # film grain effect with transparency --- NOT WORKING
    # for i in range(10):
    #     alpha_channel = int(255 - i*(255/10))
    #     pg.draw.rect(screen, Color((0, 255, 0, alpha_channel)), (i, i, WIDTH-2*i, HEIGHT-2*i), 1)

    # film grain effect (no transparency)
    pg.draw.rect(screen, Color(game.active_player.color), (0, 0, WIDTH, HEIGHT), ACTIVE_PLAYER_BAND_OUTLINE)
    
    # pg.draw.line(screen, Color('purple'), (WIDTH//2, 0), (WIDTH//2, HEIGHT))    # highlight center of screen
    
    pg.display.update()
    clock.tick(FPS)

pg.quit()

print("thanks for playing!")
