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

# Image

![BFS_Without_dead_lock](https://user-images.githubusercontent.com/68500496/201464689-6081b6f6-8ed0-45df-b6b9-1dc0c890b879.JPG)
![A_start_dead_lock_result](https://user-images.githubusercontent.com/68500496/201464693-538cfe59-cbaa-4fba-ae1e-edada69052db.JPG)


# Result
 - BFS 
    - Board1 : 11
    - Board2 : 1079
    - Board3 : 2496
    - Board4 : 6051
    - Board5 : 8446
 - A with heuristic 1 
    - Board1 : 12
    - Board2 : 1106
    - Board3 : 2489
    - Board4 : 5476
    - Board5 : 7337
 - A with heuristic 2 
    - Board1 : 9
    - Board2 : 749
    - Board3 : 1443
    - Board4 : 3098
    - Board5 : 2128
 - A with heuristic 3 
    - Board1 : 6
    - Board2 : 546
    - Board3 : 1331
    - Board4 : 2735
    - Board5 : 1539
 - A with heuristic 3 with deadlock detection
    - Board1 : 6
    - Board2 : 314
    - Board3 : 360
    - Board4 : 915
    - Board5 : 776
    - Board6 : 1009
    - Board7 : 5652
    - Board8 : 12683
    - Board9 : 18203

# Extra
 - DFS
    - Board1 : 29
    - Board2 : 1302
    - Board3 : 1974
    - Board4 : 12872
    - Board5 : 4284
 - A with heuristic 3 with deadlock detection
    - MainBoard : 12519
