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

class GameState:
    def __init__(self, map, current_cost=0):
        self.map = map
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.player = self.find_player()
        self.boxes = self.find_boxes()
        self.targets = self.find_targets()
        self.is_solved = self.check_solved()
        self.current_cost = current_cost

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to find the player, boxes, and targets in the map
    # The positions are tuples (row, column)
    # ------------------------------------------------------------------------------------------------------------------


    def find_player(self):
        """Find the player in the map and return its position"""
        # TODO: implement this method
        for i in range(0,self.height):
            for j in range(0,self.width):
                if(self.map[i][j]=="@" or self.map[i][j]=="+"):
                    return (i,j) 

    def find_boxes(self):
        """Find all the boxes in the map and return their positions"""
        boxes=[]
        for i in range(0,self.height):
            for j in range(0,self.width):
                if(self.map[i][j]=="$"):
                    boxes.append((i,j))
        return boxes 

    def find_targets(self):
        """Find all the targets in the map and return their positions"""
        targets=[]
        for i in range(0,self.height):
            for j in range(0,self.width):
                if(self.map[i][j]=="*"):
                    targets.append((i,j))
        return targets  

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
        if(self.map[position[0]][position[1]]=="$" or self.map[position[0]][position[1]]=="*"):
            return True

    def is_target(self, position):
        """Check if the given position is a target
            Note: the target can be "." or "*" (box on target)
        """
        if(self.map[position[0]][position[1]]=="." or self.map[position[0]][position[1]]=="*"):
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
        return self.current_cost + self.get_heuristic()

    def get_current_cost(self):
        """Get the current cost for the game state
            Note: the current cost is the number of moves from the initial state to the current state
        """
        return self.current_cost

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to generate the next game state and check if the game is solved
    # ------------------------------------------------------------------------------------------------------------------


    def move(self, direction):
        new_map=[list(row) for row in self.map]
        x,y=self.player
        if(direction=="U"):
            dx,dy=0,-1
        elif (direction=="R"):
            dx,dy=1,0
        elif (direction=="L"):
            dx,dy=-1,0
        elif (direction=="D"):
            dx,dy=0,1

        # dx,dy=direction
    
        #new player position
        next_x,next_y=x+dx, y+dy
        new_player_position=(next_x,next_y)
        #check player position is within bounds
        if not (0<=next_x<len(self.map) and 0<=next_y<len(self.map[0])):
            return None
        #check if player can move to an empty space or a target
        if self.is_empty(new_player_position) or self.is_target(new_player_position):
            new_map[x][y]=' ' # old position turns into empty
            if self.is_empty(new_player_position):
                new_map[next_x][next_y]='@'
            else:
                new_map[next_x][next_y]='+'
        else:
            # check if pushing box is possible
            box_x,box_y=next_x+dx,next_y+dy
            new_box_position=(box_x,box_y)
            if not (0<=box_x<len(self.map) and 0<=box_y<len(self.map[0])):
                return None
            if self.is_empty(new_box_position) or self.is_target(new_box_position):
                new_map[x][y]=' ' # old position turns into empty
                if self.is_empty(new_player_position):
                    new_map[next_x][next_y]='@'
                else:
                    new_map[next_x][next_y]='+'  
                if self.is_empty(new_box_position):
                    new_map[box_x][box_y]='$'
                else:
                    new_map[box_x][box_y]='*'
            else:
                return None # Cannot push box to wall
        new_state=GameState(new_map)
        new_state.player=new_player_position
        new_state.boxes=new_state.find_boxes()
        new_state.targets=new_state.find_targets()
        new_state.is_solved=new_state.check_solved()
        new_state.current_cost+=1
        return new_state
    
    def check_solved(self):
        return all(box in self.targets for box in self.boxes)
