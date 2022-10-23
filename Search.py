
from collections import deque
from Noeud import Node


class Search:

    @staticmethod
    def DFS(init_node: Node):
        OPEN = []
        CLOSED = []

        if init_node.state.is_goal():
            return init_node, 0
        else:
            step = 0
            OPEN.append(init_node)
            while True:
                step += 1
                if len(OPEN) <= 0:
                    return None, -1
                else:
                    current_node = OPEN.pop()
                    CLOSED.append(current_node)
                    succ = current_node.successeurs()
                    while len(succ) > 0:
                        child = succ.pop()
                        if child.state.is_goal():
                            return child, step
                        # ---- si c'est pas dans OPEN et CLOSED
                        if child.state.board_d not in [n.state.board_d for n in OPEN] and \
                                child.state.board_d not in [n.state.board_d for n in CLOSED]:
                            # ---- on l'ajoute a OPEN pour le check plus tard, et on check si c l'objectif au mieux
                            OPEN.append(child)

    @staticmethod
    def BFS(init_node: Node):
        OPEN = deque()
        CLOSED = []

        # --- si l'etat initial est l'objectif return l'etat et nombre de steps
        if init_node.state.is_goal():
            return init_node, 0
        else:
            step = 0
            # ---- on ajoute l'etat
            OPEN.append(init_node)
            while True:
                # print(f" *** Step : {step} *** ")
                step += 1
                if len(OPEN) == 0:
                    return None, -1

                # ---- on retire un etat de la liste
                current_node = OPEN.popleft()
                # ---- on l'ajoute dans closed pour dire que on l'a déjà check
                CLOSED.append(current_node)

                # ---- on calcule ses successeurs
                succ = current_node.successeurs()
                # ---- tant qu'il en a
                while len(succ) != 0:
                    # ---- on check le premiere successeur
                    child = succ.popleft()

                    # ---- si c'est pas dans OPEN et CLOSED
                    if child.state.board_d not in [n.state.board_d for n in OPEN] and \
                            child.state.board_d not in [n.state.board_d for n in CLOSED]:
                        # ---- on l'ajoute a OPEN pour le check plus tard, et on check si c l'objectif au mieux
                        OPEN.append(child)
                        if child.state.is_goal():
                            return child, step

    @staticmethod
    def AlgoTypeA(init_node: Node, heuristic=1):

        OPEN = []
        CLOSED = []
        step = 0
        # ---- si le noeud courant est l'objectif on s'arrete
        if init_node.state.is_goal():
            return init_node, 0
        else:
            # ---- sinon on calcule son heuristic et on l'ajoute
            init_node.cost_node(heuristic)
            OPEN.append(init_node)
            while True:
                # print(f" *** Step : {step} *** ")
                step += 1
                if len(OPEN) == 0:
                    return None, -1
                else:

                    # ---- on prend de OPEN le noeud ayant l'heuristique la + basse
                    min_node = OPEN[0]
                    for element in OPEN:
                        if element.costH < min_node.costH:
                            min_node = element

                    current_node = min_node

                    # ----- des que c'est fait on l'enleve de open et l'ajoute dans CLOSED
                    OPEN.remove(current_node)
                    CLOSED.append(current_node)

                    # ----- on clacule ses successeurs
                    succ = current_node.successeurs()

                    while len(succ) != 0:

                        # ----- tant qu'il en a , on prend un fils et on clacule son heuristique
                        child = succ.popleft()
                        child.cost_node(heuristic)
                        # --- si c'est l'objectif on le retourne
                        if child.state.is_goal():
                            return child, step

                        # --- sinon on l'ajoute dans OPEN si il y'ai pas

                        if child.state.board_d not in [n.state.board_d for n in OPEN] and \
                                child.state.board_d not in [n.state.board_d for n in CLOSED]:
                            OPEN.append(child)

                        # --- si il est dans OPEN ou CLOSED et minimum on update
                        elif child.state.board_d in [n.state.board_d for n in OPEN]:
                            old_child = None
                            for element in OPEN:
                                if element.state.board_d == child.state.board_d:
                                    old_child = element

                            if child.costH < old_child.costH:
                                OPEN.remove(old_child)
                                OPEN.append(child)

                        elif child.state.board_d in [n.state.board_d for n in CLOSED]:
                            old_child = None
                            for element in CLOSED:
                                if element.state.board_d == child.state.board_d:
                                    old_child = element

                            if child.costH < old_child.costH:
                                CLOSED.remove(old_child)
                                CLOSED.append(child)
