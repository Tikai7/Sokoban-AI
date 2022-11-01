# How to play
    - Press F1 to play
    - Press F2 to let the AI play
    - If you let the AI play, choose the Algorithm 
    - Press F1 for BFS
    - Press F2 for A*.
    - If you choose A*, choose Heuristics.
    - press F1,F2,F3 for the first/second/third heuristic respectively

# How it works
   - Each game state (MAP) is represented by a SokoPuzzle class.
    - They are saved and linked in a Node class where you can :
        - calculate the heuristic
        - Know the parent of the Node
        - The movements that lead to this Node
        - Whether this Node is a goal state or not
    
    - To solve the game, we use 

    - BFS algorithm
    - Algorithm A* (with deadlock detection)
    - DFS algorithm (not usable by the menu)

# Note 
    - The file "Solution.txt" contains the movements of the solutions 
        for each map and the number of steps the algorithm takes to reach the solution.
    - The best algorithm is A* with the 3rd heuristic.
