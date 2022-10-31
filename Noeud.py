
from cmath import inf
import Etat
import numpy as np
from collections import deque
from copy import deepcopy


class Node:
    def __init__(self, state: Etat.SokoPuzzle, parent=None, mouvement="", cost=1):
        self.state = state  # --- l'etat courant
        self.parent = parent  # --- le lien pere fils (l'etat d'ou on est venu)
        if self.parent == None:
            self.executed_moves = mouvement  # ---- le mouvement effectué pour etre a cet etat
            self.depth = 0  # ----- profondeur de l'etat dans lequel on est
            self.cost = 0  # -----g(n) = 0 si c'est parent
        else:
            # ---- liste d'etat qui nous ont permis d'atteindre cet etat
            self.executed_moves = self.parent.executed_moves + mouvement
            self.depth = self.parent.depth+1
            self.cost = self.parent.cost + cost  # -----g'(n) = g(n)+c(n,n')

    # ----- succecceurs d'un etat

    def successeurs(self) -> deque:
        succ = deque()
        # ---- on effectue les 4 mouvements possibles
        for m in self.state.moves.keys():
            # --- on effectue ces mouvements sur des copy
            child = deepcopy(self.state)
            child.do_move(m)
            # ----- on ajoute l'etat generer a partir du mouvement
            node_child = Node(child, self, m)
            succ.append(node_child)
        return succ

    # ----- heuristique du noeud courant
    def cost_node(self, heuristic=1):
        heuristics = {
            1: self.heuristic_1(),
            2: self.heuristic_2(),
            3: self.heuristic_3(),
            # 4: self.heuristic_4()
        }
        # f(n) = g(n)+h(n)
        self.costH = self.cost + heuristics[heuristic]

    # ----- premiere heuristique (nombre de bloques restant)

    def heuristic_1(self):
        number_left_block = 0

        for i in range(len(self.state.board_d)):
            for j in range(len(self.state.board_d[0])):
                if self.state.board_d[i][j] == "B" and self.state.board_s[i][j] != "S":
                    number_left_block += 1

        costH = number_left_block
        return costH

    def heuristic_2(self):
        cibles = np.array(self.state.board_s)
        blocks = np.array(self.state.board_d)

        B_indices_x, B_indices_y = np.where(blocks == "B")
        S_indices_x, S_indices_y = np.where(cibles == "S")

        sum_distance = 0

        for bx, by in zip(B_indices_x, B_indices_y):
            minimum_distance = inf
            for sx, sy in zip(S_indices_x, S_indices_y):
                new_distance = abs(bx-sx) + abs(by-sy)
                if minimum_distance > new_distance:
                    minimum_distance = new_distance

            sum_distance += minimum_distance

        costH = 2*self.heuristic_1() + sum_distance
        return costH

    def heuristic_3(self):
        joueur = self.state.robot_pos
        blocks = np.array(self.state.board_d)
        B_indices_x, B_indices_y = np.where(blocks == "B")
        minimum_distance = inf
        for sx, sy in zip(B_indices_x, B_indices_y):
            new_distance = abs(joueur[0]-sx) + abs(joueur[1]-sy)
            if minimum_distance > new_distance:
                minimum_distance = new_distance

        costH = self.heuristic_2()+minimum_distance
        return costH
