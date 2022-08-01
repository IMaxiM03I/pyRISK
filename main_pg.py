import pygame as pg
from constants import *
from pygame.locals import *
from assets_pg import *
from maps.classic_pg import *


### ----- VARIABLES ------ ###


game: Game = Game(classic_continents)

selected_territory: Territory = NULL_TERRITORY

# --- HUD --- #
phase_font: pg.font.Font    # "DRAFT", "ATTACK" or "FORTIFY"
phase_info_font: pg.font.Font      # display additional info related to the current phase
troops_font: pg.font.Font

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
            selected_territory = game.selectTerritory(pg.mouse.get_pos())

            if game.phase == 1 and not selected_territory.isNull():     # draft phase
                game.setFirstTerritory(selected_territory)
                if game.first_territory.ruler == game.active_player:      # selected a valid territory
                    
                    troops_to_be_added: int = int(input(f"troops drafted to {game.first_territory.name}: "))
                    troops_to_be_added = min(troops_to_be_added, game.active_player.available_troops)
                    game.first_territory.addTroops(troops_to_be_added)
                    game.active_player.removeTroops(troops_to_be_added)
                    print(f"{troops_to_be_added} troops drafted to {game.first_territory.name}", end=" ")
                    print(f"--- total: {game.first_territory.troops_stationed}")

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
    
    # --- HUD --- #
    
    # current phase #
    phase_font = pg.font.Font(None, 50)
    phase_text = phase_font.render(game.getPhaseStr(), True, TEXT_COLOR, TEXT_BG_COLOR)
    phase_text_rect = phase_text.get_rect(center=(WIDTH//2, 9*HEIGHT//10))
    screen.blit(phase_text, phase_text_rect)
    
    # selected territory's troops #
    if not selected_territory.isNull():
        troops_font = pg.font.Font(None, 50)
        troops_text = troops_font.render(str(selected_territory.troops_stationed), True, TEXT_COLOR, TEXT_BG_COLOR)
        troops_text_rect = troops_text.get_rect(center=(WIDTH//2, 19*HEIGHT//20))
        screen.blit(troops_text, troops_text_rect)
    
    # draft phase #
    if game.phase == 1:
        phase_info_font = pg.font.Font(None, 50)
        phase_info_text = phase_info_font.render(("+"+str(game.active_player.available_troops)), True, TEXT_COLOR,
                                                TEXT_BG_COLOR)
        phase_info_text_rect = phase_info_text.get_rect(center=(19*WIDTH//20, HEIGHT//2))
        screen.blit(phase_info_text, phase_info_text_rect)
    
    pg.display.update()
    clock.tick(FPS)

pg.quit()
