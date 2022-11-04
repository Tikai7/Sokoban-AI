from copy import deepcopy
import this
import numpy as np

# ---- Class designant un Etat du jeu
# ---- Un Etat change lorsque le robot se deplace


class SokoPuzzle:
    def __init__(self, board):

        # ----- Dimension matrice
        self.height = len(board)
        self.width = len(board[0])

        # ----- matrice statique
        self.board_s = self.create_matrix()
        self.board_d = self.create_matrix()
        # ----- Element static
        self.static = {"O", " ", "S"}

        # ----- Mouvement possible
        self.moves = {
            "U": (-1, 0),
            "D": (1, 0),
            "L": (0, -1),
            "R": (0, 1)
        }
        # ----- Mouvement impossible

        self.illegal_moves = {"B", "O"}
        self.robot_pos = (3, 2)

        # ----- Division de la map en 2 sous maps - dynamic et static
        for i, line in enumerate(board):
            for j, element in enumerate(line):
                if element in self.static:
                    self.board_s[i][j] = element
                elif element == "R":
                    self.board_d[i][j] = element
                    self.robot_pos = (i, j)
                elif element == "S":
                    self.board_s[i][j] = element
                elif element == ".":
                    self.robot_pos = (i, j)
                    self.board_s[i][j] = "S"
                    self.board_d[i][j] = "R"
                elif element == "*":
                    self.board_d[i][j] = "B"
                    self.board_s[i][j] = "S"
                else:
                    self.board_s[i][j] = " "
                    self.board_d[i][j] = "B"

        self.board_dead = self.create_deadlock()
        # self.show_deadlock_map()

    # ------ Fonction calculant la nouvelle pos du joueur dans la map

    def direction(self, tuples):

        r_x, r_y = self.robot_pos
        r_x += tuples[0]
        r_y += tuples[1]

        if self.board_s[r_x][r_y] == "O":
            return False
        elif self.board_d[r_x][r_y] != "B":
            self.robot_pos = (r_x, r_y)
            self.board_d[r_x][r_y] = "R"
            self.board_d[r_x-tuples[0]][r_y-tuples[1]] = " "

            return True
        elif self.board_d[r_x+tuples[0]][r_y+tuples[1]] != "B" and self.board_s[r_x+tuples[0]][r_y+tuples[1]] != "O":
            self.robot_pos = (r_x, r_y)
            self.board_d[r_x-tuples[0]][r_y-tuples[1]] = " "
            self.board_d[r_x][r_y] = "R"
            self.board_d[r_x+tuples[0]][r_y+tuples[1]] = "B"

            return True

        return False

    def is_deadlock(self):
        dynamic_board = np.array(self.board_d)
        bx, by = np.where(dynamic_board == "B")

        for x, y in zip(bx, by):
            if self.board_dead[x][y] == "D":
                return True

        return False

    # ------ Fonction crée une matrice de deadlocks

    def create_deadlock(self):
        board_dead = self.create_matrix()
        for i in range(1, len(self.board_s)-1):
            for j in range(1, len(self.board_s[0])-1):
                if self.is_corner_deadlock(i, j):
                    board_dead[i][j] = "D"

        board_dead = self.detect_line_dead_lock(board_dead)
        return board_dead

    # ------ Fonction qui verifie si le block est un deadlock de coins
    def detect_line_dead_lock(self, board_dead):

        dont_verif = {"S", "O"}

        left_line = True
        right_line = True
        top_line = True
        bottom_line = True

        corners_dead_locks = np.array(board_dead)
        dx, dy = np.where(corners_dead_locks == "D")
        new_dx = dx[1:]
        new_dy = dy[1:]

        for indice_x, indice_y in zip(dx, dy):
            for indice_i, indice_j in zip(new_dx, new_dy):
                if indice_i == indice_x and indice_j != indice_y:

                    counter = indice_y
                    counter_deb = indice_j

                    if indice_j > indice_y:
                        counter = indice_j
                        counter_deb = indice_y

                    for col in range(counter):
                        if self.board_s[indice_x][col] not in dont_verif:
                            if self.board_s[indice_x+1][col] != "O":
                                bottom_line = False
                            if self.board_s[indice_x-1][col] != "O":
                                top_line = False

                    i_can_add = True
                    if bottom_line or top_line:
                        for j in range(counter_deb, counter):
                            if self.board_s[indice_x][j] in dont_verif:
                                i_can_add = False

                        for j in range(counter_deb, counter):
                            if i_can_add and self.board_s[indice_x][j] not in dont_verif:
                                board_dead[indice_x][j] = "D"

                if indice_j == indice_y and indice_i != indice_x:
                    counter = indice_x
                    counter_deb = indice_i
                    if indice_i > indice_x:
                        counter = indice_i
                        counter_deb = indice_x

                    for row in range(counter):
                        if self.board_s[row][indice_y] not in dont_verif:
                            if self.board_s[row][indice_y+1] != "O":
                                right_line = False
                            if self.board_s[row][indice_y-1] != "O":
                                left_line = False

                    i_can_add = True

                    if left_line or right_line:
                        for i in range(counter_deb, counter):
                            if self.board_s[i][indice_y] in dont_verif:
                                i_can_add = False

                        for i in range(counter_deb, counter):
                            if i_can_add and self.board_s[i][indice_y] not in dont_verif:
                                board_dead[i][indice_y] = "D"

            left_line = True
            right_line = True
            top_line = True
            bottom_line = True

        return board_dead
    # ------ Fonction qui verifie si le block est un deadlock de coins

    def is_corner_deadlock(self, x, y):

        dont_verif = {"S", "O"}
        horizontal_move = False
        vertical_move = False

        if self.board_s[x][y] not in dont_verif:
            if self.board_s[x+1][y] == "O" or self.board_s[x-1][y] == "O":
                horizontal_move = True
            if self.board_s[x][y+1] == "O" or self.board_s[x][y-1] == "O":
                vertical_move = True

        return horizontal_move and vertical_move

    # ------ Fonction confirmant que le noeud objectif est atteinds

    def is_goal(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board_s[i][j] == "S" and self.board_d[i][j] != "B":
                    return False

        return True

    # ----- Fonction qui execute les mouvements

    def do_move(self, m):
        return self.direction(self.moves[m])

    def show_deadlock_map(self):
        print("**********************")
        for line_d, line_s in zip(self.board_dead, self.board_s):
            for col_d, col_s in zip(line_d, line_s):
                if col_d == ' ':
                    print(col_s, end=" ")
                else:
                    print(col_d, end=" ")
            print("\n")
    # ------ Fonction affichant les matrices

    def show_matrix(self):
        print("**********************")
        for line_d, line_s in zip(self.board_d, self.board_s):
            for col_d, col_s in zip(line_d, line_s):
                if col_d == ' ':
                    print(col_s, end=" ")
                else:
                    print(col_d, end=" ")
            print("\n")

    # ------ Fonction creant des matrices

    def create_matrix(self):
        mat = []
        for _ in range(self.height):
            line = []
            for _ in range(self.width):
                line.append(' ')
            mat.append(line)
        return mat
