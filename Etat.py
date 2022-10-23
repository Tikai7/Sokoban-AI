

#---- Class designant un Etat du jeu
#---- Un Etat change lorsque le robot se deplace

class SokoPuzzle:
    def __init__(self,board):

        #----- Dimension matrice
        self.height=len(board)
        self.width=len(board[0])

        #----- matrice statique
        self.board_s=self.create_matrix()
        self.board_d=self.create_matrix()

        #----- Element static 
        self.static = {"O"," ","S"}

        #----- Mouvement possible  
        self.moves = {
            "U":(-1,0),
            "D":(1,0),
            "L":(0,-1),
            "R":(0,1)
        }
        #----- Mouvement impossible  

        self.illegal_moves={"B","O"}
        self.robot_pos=(3,2)

        #----- Division de la map en 2 sous maps - dynamic et static
        for i,line in enumerate(board):
            for j,element in enumerate(line):
                if element in self.static:
                    self.board_s[i][j]=element
                elif element == "R":
                    self.board_d[i][j]=element
                    self.robot_pos=(i,j)
                elif element == "S":
                    self.board_s[i][j]=element
                elif element == ".":
                    self.robot_pos=(i,j)
                    self.board_s[i][j]="S"
                    self.board_d[i][j]="R"
                elif element == "*":
                    self.board_d[i][j]="B"
                    self.board_s[i][j]="S"
                else:
                    self.board_s[i][j]=" "
                    self.board_d[i][j]="B"


    #------ Fonction calculant la nouvelle pos du joueur dans la map
    def direction(self,tuples):
        
        r_x,r_y = self.robot_pos
        r_x+=tuples[0]
        r_y+=tuples[1]

        if self.board_s[r_x][r_y] == "O" :
            return False
        elif self.board_d[r_x][r_y] != "B":
            self.robot_pos=(r_x,r_y)
            self.board_d[r_x][r_y]="R"
            self.board_d[r_x-tuples[0]][r_y-tuples[1]]=" "
            return True
        elif self.board_d[r_x+tuples[0]][r_y+tuples[1]] != "B" and self.board_s[r_x+tuples[0]][r_y+tuples[1]] != "O":
            self.robot_pos=(r_x,r_y)
            self.board_d[r_x-tuples[0]][r_y-tuples[1]]=" "
            self.board_d[r_x][r_y]="R"
            self.board_d[r_x+tuples[0]][r_y+tuples[1]]="B"
    
            return True
        
        return False


    #------ Fonction confirmant que le noeud objectif est atteinds
    def is_goal(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board_s[i][j] == "S" and self.board_d[i][j] != "B":
                    return False
                    
        return True

    #----- Fonction qui execute les mouvements

    def do_move(self,m):
        return self.direction(self.moves[m])


    #------ Fonction affichant les matrices
    def show_matrix(self):
        print("**********************")
        for line_d,line_s in zip(self.board_d,self.board_s):
            for col_d,col_s in zip(line_d,line_s):
                if col_d == ' ':
                    print(col_s,end=" ")
                else:
                    print(col_d,end=" ")
            print("\n")


    #------ Fonction creant des matrices
    def create_matrix(self):
        mat = []
        for _ in range(self.height):
            line = []
            for _ in range(self.width):
                line.append(' ')
            mat.append(line)
        return mat