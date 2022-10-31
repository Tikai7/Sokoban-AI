
from collections import deque
from Noeud import Node


class Search:

    @staticmethod
    def DFS(init_node: Node, max_depth):
        OPEN = []
        CLOSED = []

        if init_node.state.is_goal():
            return init_node, 0
        else:
            step = 0
            OPEN.append(init_node)
            while True and max_depth <= init_node.depth:
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

        OPEN = deque()
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
                    OPEN = deque(
                        sorted(list(OPEN), key=lambda noeud: noeud.costH))
                    current_node = OPEN.popleft()

                    # ----- des que c'est fait on l'enleve de open et l'ajoute dans CLOSED
                    CLOSED.append(current_node)

                    # ----- on clacule ses successeurs
                    succ = current_node.successeurs()
                    # --- si c'est l'objectif on le retourne
                    if current_node.state.is_goal():
                        return current_node, step

                    while len(succ) != 0:

                        # ----- tant qu'il en a , on prend un fils et on calcule son heuristique
                        child = succ.popleft()

                        if not child.state.is_deadlock():
                            child.cost_node(heuristic)

                            # --- sinon on l'ajoute dans OPEN si il y'ai pas

                            if child.state.board_d not in [n.state.board_d for n in OPEN] and \
                                    child.state.board_d not in [n.state.board_d for n in CLOSED]:
                                OPEN.append(child)

                            # --- si il est dans OPEN ou CLOSED et minimum on update
                            elif child.state.board_d in [n.state.board_d for n in OPEN]:
                                index = [n.state.board_d for n in OPEN].index(
                                    child.state.board_d)

                                if child.costH < OPEN[index].costH:
                                    OPEN.remove(OPEN[index])
                                    OPEN.append(child)

                            elif child.state.board_d in [n.state.board_d for n in CLOSED]:
                                index = [n.state.board_d for n in CLOSED].index(
                                    child.state.board_d)

                                if child.costH < CLOSED[index].costH:
                                    CLOSED.remove(CLOSED[index])
                                    OPEN.append(child)
