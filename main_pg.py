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
            
            if event.key == K_RETURN:
                if game.phase != 1:     # can't skip DRAFT phase
                    game.passPhase()
                    selected_territory = NULL_TERRITORY     # reset UI
        
        elif event.type == MOUSEBUTTONUP:
            selected_territory = game.selectTerritory(pg.mouse.get_pos())

            if game.phase == 1 and not selected_territory.isNull():     # draft phase
                game.setFirstTerritory(selected_territory)
                if game.first_territory.ruler == game.active_player:      # selected a valid territory
                    game.draftTroops()
                    
                    # check if draft phase is over
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
    
    # --- UI --- #
    
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
    pg.draw.rect(screen, Color(game.active_player.color), (0, 0, WIDTH, HEIGHT), 10)
    
    # current phase #
    phase_font = pg.font.Font(None, FONT_SIZE)
    phase_text = phase_font.render(game.getPhaseStr(), True, TEXT_COLOR, TEXT_BG_COLOR)
    phase_text_rect = phase_text.get_rect(center=(WIDTH//2, 9*HEIGHT//10))
    screen.blit(phase_text, phase_text_rect)
    
    # selected territory's troops #
    if not selected_territory.isNull():
        troops_font = pg.font.Font(None, FONT_SIZE)
        if selected_territory.ruler.color != "black":
            troops_text = troops_font.render(f"{selected_territory.name}: {str(selected_territory.troops_stationed)}",
                                             True, Color(selected_territory.ruler.color), TEXT_BG_COLOR)
        else:
            troops_text = troops_font.render(f"{selected_territory.name}: {str(selected_territory.troops_stationed)}",
                                             True, Color(selected_territory.ruler.color), "white")
        troops_text_rect = troops_text.get_rect(center=(WIDTH//2, 19*HEIGHT//20))
        screen.blit(troops_text, troops_text_rect)
    
    # draft phase #
    if game.phase == 1:
        phase_info_font = pg.font.Font(None, FONT_SIZE)
        phase_info_text = phase_info_font.render(("+"+str(game.active_player.available_troops)), True, TEXT_COLOR,
                                                 TEXT_BG_COLOR)
        phase_info_text_rect = phase_info_text.get_rect(center=(19*WIDTH//20, HEIGHT//2))
        screen.blit(phase_info_text, phase_info_text_rect)
    
    pg.display.update()
    clock.tick(FPS)

pg.quit()
