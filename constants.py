import pygame as pg
from pygame.locals import *
from math import sin, pi

# SCREEN #
SCREEN_SIZE: int = 500
WIDTH: int = 1000
HEIGHT: int = 647
FPS: int = 60

# MAP #
BG_COLOR: Color = Color("white")
TERRITORY_MARKER_RADIUS: int = WIDTH//75
ATTACKER_MARKER_SIDE_LENGTH: int = int(2 * TERRITORY_MARKER_RADIUS * (sin(2*pi/3) / sin(pi/6)))		# math

# TEXT #
FONT_SIZE: int = 35
TEXT_COLOR: str = "white"
TEXT_BG_COLOR: str = "black"

DARK_COLORS: list[str] = ["black", "red", "blue", "purple"]

# CARDS #
CARD_WIDTH: int = WIDTH//15
CARD_HEIGHT: int = HEIGHT//10
CARD_COLOR: str = "red"
CARD_BG_COLOR: str = "white"
MISSION_CARD_COORDS: tuple[int, int] = (WIDTH//10, 4*HEIGHT//5)
TERRITORY_CARD_COORDS: tuple[int, int] = (WIDTH//10, 9*HEIGHT//10)
CARD_FONT_SIZE: int = 50

# CARDS VIEW SCREEN #
CARDS_VIEW_WIDTH: int = 2*WIDTH//3
CARDS_VIEW_HEIGHT: int = 2*HEIGHT//3

CARDS_EXIT_COORDS: tuple[int, int] = (19*WIDTH//20, HEIGHT//15)
CARDS_EXIT_RADIUS: int = 2 * TERRITORY_MARKER_RADIUS

SELECTED_SLOT_BG_COLOR: str = "darkgrey"
SELECTED_SLOT_COLOR: str = "black"
coefficients: tuple[float, float, float] = (-2, -0.5, 1) 	# math
SELECTED_SLOT_Y: int = HEIGHT//10
SELECTED_SLOT_WIDTH: int = 3*WIDTH//20
SELECTED_SLOT_X_COORDS: list[int] = [WIDTH//2 + int(coefficients[i] * SELECTED_SLOT_WIDTH) for i in range(len(coefficients))] 	# math
SELECTED_SLOT_HEIGHT: int = 3*HEIGHT//10

PLAYER_CARD_BG_COLOR: str = "red"
PLAYER_CARD_OUTLINE_COLOR: str = "darkred"
PLAYER_CARD_TEXT_COLOR: str = "black"
PLAYER_CARD_WIDTH: int = WIDTH//10
PLAYER_CARD_HEIGHT: int = HEIGHT//4
PLAYER_CARD_Y: int = 13 * HEIGHT//20

TRADE_BUTTON_CENTER: tuple[int, int] = (WIDTH//2 + (SELECTED_SLOT_X_COORDS[-1] + SELECTED_SLOT_WIDTH)//2, SELECTED_SLOT_Y//2 + SELECTED_SLOT_HEIGHT//2)
TRADE_BUTTON_WIDTH: int = 2 * (WIDTH - (SELECTED_SLOT_X_COORDS[-1] + SELECTED_SLOT_WIDTH)) // 3
TRADE_BUTTON_HEIGHT: int = 4 * FONT_SIZE // 3
TRADE_BUTTON_COORDS: tuple[int, int] = (TRADE_BUTTON_CENTER[0] - TRADE_BUTTON_WIDTH//2, TRADE_BUTTON_CENTER[1] - TRADE_BUTTON_HEIGHT//2)
TRADE_BUTTON_BG_COLOR: str = "black"
TRADE_BUTTON_OUTLINE_COLOR: str = "green"
TRADE_BUTTON_TEXT_COLOR: str = "green"

# OTHER #
FIRST_TRADES_TROOPS: list[int] = [4, 6, 8, 10, 12, 15]
