import pygame as pg
from constants import *
from pygame.locals import *
from assets_pg import *
from maps.classic_pg import *



### ----- VARIABLES ------ ###



game: Game = Game(classic_continents)

# --- pygame --- #

pg.init()
screen: pg.Surface = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("shitty RISK")

clock: pg.time.Clock = pg.time.Clock()

running: bool = True



### ------ FUNCTIONS ------ ###



### ------ CLASSES ------ ###



### ------ MAIN ------ ###



while running:

    for event in pg.event.get():

        if event.type == QUIT:
            running = False
        
        elif event.type == KEYUP:

            if event.key == K_ESCAPE:
                running = False
            
            if event.key == K_KP_ENTER:
                if game.phase == 2:     # attack phase
                    game.passPhase()
        
        elif event.type == MOUSEBUTTONUP:
            selected_territory: Territory = game.selectTerritory(pg.mouse.get_pos())
            # if selected_territory is None:
            #     print(None)
            # else:
            #     print(selected_territory.name)

            if game.phase == 1 and selected_territory is not None:     # draft phase
                if selected_territory.ruler == game.active_player:      # selected a valid territory
                    
                    troops_to_be_added: int = int(input(f"troops drafted to {selected_territory.name}: "))
                    troops_to_be_added = min(troops_to_be_added, game.active_player.available_troops)
                    selected_territory.addTroops(troops_to_be_added)
                    game.active_player.removeTroops(troops_to_be_added)
                    print(f"{troops_to_be_added} troops drafted to {selected_territory.name} --- total: {selected_territory.troops_stationed}")

                    if game.active_player.available_troops > 0:
                        print(f"{game.active_player.available_troops} troops left to be added")
                    print()

                    if game.active_player.available_troops == 0:
                        game.passPhase()
            
            elif game.phase == 2:     # attack phase
                if selected_territory.ruler == game.active_player:
                    game.setFirstTerritory(selected_territory)
                elif game.hasSelectedFirstTerritory():
                    game.attack(selected_territory)

    # REFRESH #
    
    # --- map --- #

    screen.fill(BG_COLOR)
    screen.blit(CLASSIC_MAP, (0, 0))

    game.drawTerritories(screen)

    pg.display.update()
    clock.tick(FPS)

pg.quit()