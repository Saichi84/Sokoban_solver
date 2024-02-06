"""
Sokuban game state class
The state of the game consists the map which is a 2D array of characters. There are 6 types of characters:
- ' ': empty space
- '#': wall
- '$': box
- '.': target
- '@': player
- '+': player on target
- '*': box on target
The game state class keeps track of the map.
The game state also keeps track of the player and box positions, and whether the game is solved or not.
The game state class has the following methods:
- find_player(): find the player in the map and return its position
- find_boxes(): find all the boxes in the map and return their positions
- find_targets(): find all the targets in the map and return their positions  
- generate_next_state(direction): generate the next game state by moving the player to the given direction
- check_solved(): check if the game is solved
"""
import numpy as np

class GameState:
    def __init__(self, map, current_cost=0):
        self.map = map
        self.player = self.find_player()
        self.boxes = self.find_boxes()
        self.targets = self.find_targets()
        self.is_solved = self.check_solved()
        self.current_cost = current_cost
        self.height = len(self.map)
        self.width = len(self.map[0])

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to find the player, boxes, and targets in the map
    # The positions are tuples (row, column)
    # ------------------------------------------------------------------------------------------------------------------


    def find_player(self):
        """Find the player in the map and return its position"""
        # TODO: implement this method
        for i in range(0,self.height):
            for j in range(0,self.width):
                if(self.map[i][j]=="@"):
                    return tuple(i,j) 

    def find_boxes(self):
        """Find all the boxes in the map and return their positions"""
        for i in range(0,self.height):
            for j in range(0,self.width):
                if(self.map[i][j]=="$"):
                    return tuple(i,j) 

    def find_targets(self):
        """Find all the targets in the map and return their positions"""
        for i in range(0,self.height):
            for j in range(0,self.width):
                if(self.map[i][j]=="*"):
                    return tuple(i,j) 

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to check if a position is a wall, box, target, or empty space
    # The position is a tuple (row, column)
    # ------------------------------------------------------------------------------------------------------------------

    def is_wall(self, position):
        """Check if the given position is a wall"""
        if(self.map[position[0]][position[1]]=="#"):
            return True

    def is_box(self, position):
        """Check if the given position is a box
            Note: the box can be on "$" or "*" (box on target)
        """
        if(self.map[position[0]][position[1]]=="$" | self.map[position[0]][position[1]]=="*"):
            return True

    def is_target(self, position):
        """Check if the given position is a target
            Note: the target can be "." or "*" (box on target)
        """
        if(self.map[position[0]][position[1]]=="." | self.map[position[0]][position[1]]=="*"):
            return True

    def is_empty(self, position):
        """Check if the given position is empty"""
        if(self.map[position[0]][position[1]]==" "):
            return True

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods get heuristics for the game state (for informed search strategies)
    # ------------------------------------------------------------------------------------------------------------------

    def get_heuristic(self):
        """Get the heuristic for the game state
            Note: the heuristic is the sum of the distances from all the boxes to their nearest targets
        """
        heuristic=0
        for box in self.boxes:
            min_distance=float('inf')
            for target in self.targets:
                distance=abs(box[0]-target[0])+abs[box[1]-target[1]]
                min_distance=min(min_distance,distance)
            heuristic+=min_distance
        return heuristic 
        

    def get_total_cost(self):
        """Get the cost for the game state
            Note: the cost is the number of moves from the initial state to the current state + the heuristic
        """
        pass

    def get_current_cost(self):
        """Get the current cost for the game state
            Note: the current cost is the number of moves from the initial state to the current state
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to generate the next game state and check if the game is solved
    # ------------------------------------------------------------------------------------------------------------------

    def move(self, direction):
        dx, dy = direction
        x, y = self.player
        next_x, next_y = x + dx, y + dy

        if self.is_wall((next_x, next_y)):
            return None
        
        if self.is_box(next_x, next_y):
            if not self.move_box(next_x, next_y, dx, dy):
                return None
        
        self.player = (next_x, next_y)
        self.current_cost += 1

        self.update_map()
        self.is_solved = self.check_solved()
        return self

    def is_box(self, x, y):
        return (x, y) in self.boxes
    
    def move_box(self , x ,y , dx , dy) : 
        next_x , next_y = x + dx , y + dy
        if self.is_wall(next_x, next_y) or self.is_box(next_x , next_y) : 
            return False

    def update_map(self):
        x, y = self.player
        self.map[x][y] = '@' if self.map[x][y] == ' ' else '+'
        for box in self.boxes:
            x, y = box
            self.map[x][y] = '$' if self.map[x][y] == ' ' else '*' 
    
    def check_solved(self):
        return all(box in self.targets for box in self.boxes)
    
    # return GameState(self.map, self.current_cost + 1)
