

import math
import time
import Etat
import pygame
import Noeud
from Search import Search
from collections import deque

pygame.font.init()
# ----- Image du joueur
IMAGES = {
    "U": "./assets/Player/player_08.png",
    "D": "./assets/Player/player_23.png",
    "L": "./assets/Player/player_20.png",
    "R": "./assets/Player/player_11.png",
}

CASES = {
    "R":   "./assets/Ground/ground_06.png",
    "O":   "./assets/Blocks/block_07.png",
    " ":   "./assets/Ground/ground_06.png",
    "S":   "./assets/Ground/ground_03.png",
    "B":   "./assets/Crates/crate_02.png",
    "*":   "./assets/Crates/crate_04.png"
}


def render_static(surface, board_s):
    for row_index, row in enumerate(board_s):
        for col_index, column in enumerate(row):
            position_x = col_index*64
            position_y = row_index*64
            asset = pygame.image.load(
                CASES[column]).convert_alpha()
            surface.blit(asset, (position_x, position_y))


def render_dynamic(surface, board_d, board_s, orientation):
    legale_moves = {"B", "*"}
    for row_index, row in enumerate(board_d):
        for col_index, column in enumerate(row):
            position_x = col_index*64
            position_y = row_index*64

            asset = pygame.image.load(
                CASES[board_s[row_index][col_index]]).convert_alpha()
            surface.blit(asset, (position_x, position_y))

            if column == "R":
                asset = pygame.image.load(orientation).convert_alpha()
                surface.blit(asset, (position_x, position_y))
            elif column == "B" and board_s[row_index][col_index] == "S":
                asset = pygame.image.load(
                    CASES["*"]).convert_alpha()
                surface.blit(asset, (position_x, position_y))
            elif column in legale_moves:
                asset = pygame.image.load(
                    CASES[column]).convert_alpha()
                surface.blit(asset, (position_x, position_y))

# ---- Cette matrice peut etre separer en deux matrice
# ---- Matrice des objets dynamique (S et JOUEUR)
# ---- Matrice des objets statique


board = [
    ["O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", " ", " ", " ", "O", "O"],
    ["O", ".", " ", "B", " ", " ", "O", "O"],
    ["O", "O", "O", " ", "B", " ", "O", "O"],
    ["O", "S", "O", "O", " ", " ", "O", "O"],
    ["O", " ", "O", " ", "S", " ", "O", "O"],
    ["O", "B", " ", "*", "B", "B", "S", "O"],
    ["O", " ", " ", " ", "S", " ", " ", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O"],
]

board1 = [['O', 'O', 'O', 'O', 'O', 'O'],
          ['O', 'S', ' ', 'B', ' ', 'O'],
          ['O', ' ', 'O', 'R', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', 'O'],
          ['O', 'O', 'O', 'O', 'O', 'O']]

board2 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
          ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
          ['O', ' ', ' ', 'O', 'O', 'O', ' ', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', 'O', '.', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
          ['O', ' ', ' ', 'B', ' ', ' ', 'O', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
          ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

board3 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
          ['O', ' ', ' ', ' ', 'O', ' ', ' ', 'O'],
          ['O', ' ', ' ', 'B', 'R', ' ', ' ', 'O'],
          ['O', ' ', ' ', ' ', 'O', 'B', ' ', 'O'],
          ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
          ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
          ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

board4 = [['O', 'O', 'O', 'O', 'O', 'O', 'O'],
          ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
          ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
          ['O', 'O', ' ', '*', ' ', ' ', 'O'],
          ['O', 'O', 'B', 'O', 'B', ' ', 'O'],
          ['O', ' ', 'S', 'R', 'S', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', 'O', 'O'],
          ['O', 'O', 'O', ' ', ' ', 'O', 'O'],
          ['O', 'O', 'O', 'O', 'O', 'O', 'O']]

board5 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
          ['O', 'O', 'O', 'S', 'O', ' ', ' ', 'O', 'O'],
          ['O', ' ', ' ', ' ', ' ', 'B', ' ', 'O', 'O'],
          ['O', ' ', 'B', ' ', 'R', ' ', ' ', 'S', 'O'],
          ['O', 'O', 'O', ' ', 'O', ' ', 'O', 'O', 'O'],
          ['O', 'O', 'O', 'B', 'O', ' ', 'O', 'O', 'O'],
          ['O', 'O', 'O', ' ', ' ', 'S', 'O', 'O', 'O'],
          ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]


Launch = True
Menu = True
MenuAlgo = False
MenuHeur = False
Player = False
AI = False

FIRSTIME = True


WIDTH = len(board[0])*64
HEIGHT = len(board)*64

surface = pygame.display.set_mode((WIDTH, HEIGHT))  # pygame.RESIZABLE
surface.fill((155, 155, 155))


Algorithme = ""
heuristic = ""
orientation = IMAGES["D"]
k = 0

while Launch:

    while Menu:
        # surface.fill((115, 162, 255))
        asset = pygame.image.load("./assets/Menu/MENU.png").convert_alpha()
        asset = pygame.transform.scale(asset, (WIDTH, HEIGHT))
        surface.blit(asset, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Menu = False
                Launch = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    Menu = False
                    Player = True
                    surface.fill((155, 155, 155))
                    pygame.display.flip()
                elif event.key == pygame.K_F2:
                    AI = True
                    Menu = False
                    MenuAlgo = True
                    surface.fill((155, 155, 155))
                    pygame.display.flip()

    while MenuAlgo:
        asset = pygame.image.load(
            "./assets/Menu/MENU_ALGO.png").convert_alpha()
        asset = pygame.transform.scale(asset, (WIDTH, HEIGHT))
        surface.blit(asset, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MenuAlgo = False
                Menu = True
                Launch = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    Algorithme = "BFS"
                    MenuAlgo = False
                    surface.fill((155, 155, 155))
                    pygame.display.flip()
                elif event.key == pygame.K_F2:
                    Algorithme = "AlgoTypeA"
                    MenuAlgo = False
                    MenuHeur = True
                    surface.fill((155, 155, 155))
                    pygame.display.flip()

    while MenuHeur:
        asset = pygame.image.load(
            "./assets/Menu/MENU_HEUR.png").convert_alpha()
        asset = pygame.transform.scale(asset, (WIDTH, HEIGHT))
        surface.blit(asset, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Launch = False
                MenuHeur = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    heuristic = 1
                    MenuHeur = False
                    surface.fill((155, 155, 155))
                    pygame.display.flip()
                elif event.key == pygame.K_F2:
                    heuristic = 2
                    MenuHeur = False
                    surface.fill((155, 155, 155))
                    pygame.display.flip()
                elif event.key == pygame.K_F3:
                    heuristic = 3
                    MenuHeur = False
                    surface.fill((155, 155, 155))
                    pygame.display.flip()

    while Player:

        if FIRSTIME:
            boards = [board1, board2, board3, board4, board5]
            FIRSTIME = False
            Game = Etat.SokoPuzzle(boards[k])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Player = False
                Launch = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z or event.key == pygame.K_UP:
                    Game.do_move("U")
                    orientation = IMAGES["U"]
                elif event.key == pygame.K_q or event.key == pygame.K_LEFT:
                    Game.do_move("L")
                    orientation = IMAGES["L"]
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    Game.do_move("R")
                    orientation = IMAGES["R"]
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    Game.do_move("D")
                    orientation = IMAGES["D"]

        if Game.is_goal():
            FIRSTIME = True
            k += 1
            surface.fill((155, 155, 155))
            pygame.display.flip()
            Game = Etat.SokoPuzzle(boards[k])

        render_dynamic(surface, Game.board_d, Game.board_s, orientation)
        pygame.display.flip()

    while AI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                AI = False
                Launch = False

        if FIRSTIME:
            boards = [board1, board2, board3, board4, board5]
            FIRSTIME = False
            Game = Etat.SokoPuzzle(boards[k])
            init_node = Noeud.Node(Game)

            deb = time.time()
            if Algorithme == "BFS":
                node, step = Search.BFS(init_node)
            else:
                node, step = Search.AlgoTypeA(init_node, heuristic)
            fin = time.time()

            print(f"Nombre de mouvement : {step}")
            print(f"Mouvement a faire : {node.executed_moves}")

            text = f"Steps : {step} Time : {math.ceil(fin-deb)}s"
            text_font = pygame.font.SysFont("Comic Sans MS", 30)
            text_render = text_font.render(text, False, (255, 255, 255))

            IA_moves = str(node.executed_moves)
            # with open("solution.txt", "a") as fichier:
            #     fichier.write(f"{IA_moves} \t Step : {step} \n")

            IA_moves = [x for x in IA_moves]
            IA_moves = deque(IA_moves)

        if len(IA_moves) > 0:
            move = IA_moves.popleft()
            Game.do_move(move)
            orientation = IMAGES[move]
        else:
            FIRSTIME = True
            k += 1
            surface.fill((155, 155, 155))
            pygame.display.flip()
            Game = Etat.SokoPuzzle(boards[k])

        # ------------------------ RENDY PYGAME DE LA MAP DYNAMIQUE
        render_dynamic(surface, Game.board_d, Game.board_s, orientation)
        surface.blit(text_render, (0, 0))
        pygame.display.flip()
        time.sleep(0.2)
