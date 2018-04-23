#
'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''

import simpleai.search
from simpleai.search import SearchProblem, breadth_first
from simpleai.search.viewers import WebViewer

# --------------- State Definition -----------------

class GameState:
        
    def __init__(self, position, goals):
        self.position  = position # tuple (x,y)
        self.goals = goals # list of [(x1,y1), (x2, y2), ...]

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, GameState)

    def __str__(self):
        return "State: < %s %s > " % (self.position, self.goals)

    def update(self, action):
        # update position
        if action is "East":
            self.position = (self.position[0]+1, self.position[1]) 
        elif action is "West":
            self.position = (self.position[0]-1, self.position[1])
        elif action is "North":
            self.position = (self.position[0], self.position[1]+1)
        elif action is "South":
            self.position = (self.position[0], self.position[1]-1)

        # if at goal, mark as visited
        if self.position in goals:
            goals.remove()  
        

# --------------- GameProblem Definition -----------------

class GameProblem(SearchProblem):

    # Object attributes, can be accessed in the methods below
    
    MAP=None
    POSITIONS=None
    INITIAL_STATE=None
    GOAL=None
    CONFIG=None
    AGENT_START=None
    ALGORITHM=None

    # --------------- Common functions to a SearchProblem -----------------
    
    
    def actions(self, state):
        
        '''Returns a LIST of the actions that may be executed in this state
        '''
        actions = []
        pos = state.position
        pos_east = (pos[0]+1, pos[1])
        pos_west = (pos[0]-1, pos[1])
        pos_north = (pos[0], pos[1]+1)
        pos_south = (pos[0], pos[1]-1)
        
        if self.can_fly(pos_east):
            actions.append('East')
        if self.can_fly(pos_west):
            actions.append('West')
        if self.can_fly(pos_north):
            actions.append('North')
        if self.can_fly(pos_south):
            actions.append('South')
        
        return actions
    
    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''
        return state.update(action)

    def is_goal(self, state):
        '''Returns true if state is the final state
        ''' 
        return state == self.GOAL

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        return 1

    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''
        return 0

    def setup (self):

        base = self.CONFIG.get("agentInit")
        goals = self.POSITIONS.get("goal")

        initial_state = GameState(base, goals)
        final_state = GameState(base, [])
        algorithm = breadth_first   
        
        return initial_state,final_state,algorithm

    # --------------- Helper Methods  ----------------- #
    
    def can_fly(self, position):
        print(self.CONFIG)  
        map = self.CONFIG.get("map_size")

        if 0 <= position[0] < map[0] and 0 <= position[1] <= map[1]:  
            return self.MAP[position[0]][position[1]][1] is not "sea"
        return False

    # -------------------------------------------------------------- #
    # --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
    # -------------------------------------------------------------- #
    
    def getAttribute (self, position, attributeName):
        '''Returns an attribute value for a given position of the map
           position is a tuple (x,y)
           attributeName is a string
           
           Returns:
               None if the attribute does not exist
               Value of the attribute otherwise
        '''
        print(position[1])
        tileAttributes=self.MAP[position[0]][position[1]][2]
        if attributeName in tileAttributes.keys():
            return tileAttributes[attributeName]
        else:
            return None
        
    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
    def initializeProblem(self,map,positions,conf,aiBaseName):
        print("SETUP #1")

        # Loads the problem attributes: self.AGENT_START, self.POSITIONS,etc.
        if self.mapInitialization(map,positions,conf,aiBaseName):
            print("SETUP #2")
            initial_state,final_state,algorithm = self.setup()
            
            self.INITIAL_STATE=initial_state
            self.GOAL=final_state
            self.ALGORITHM=algorithm
            super(GameProblem,self).__init__(self.INITIAL_STATE)
            
            return True
        else:
            return False
        
    # END initializeProblem 


    def mapInitialization(self,map,positions,conf,aiBaseName):
        # Creates lists of positions from the configured map
        # The initial position for the agent is obtained from the first and only aiBaseName tile
        self.MAP=map
        self.POSITIONS=positions
        self.CONFIG=conf

        if 'agentInit' in conf.keys():
            self.AGENT_START = tuple(conf['agentInit'])
        else:                    
            if aiBaseName in self.POSITIONS.keys():
                if len(self.POSITIONS[aiBaseName]) == 1:
                    self.AGENT_START = self.POSITIONS[aiBaseName][0]
                else:
                    print ('-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}", found several at {1}'.format(aiAgentName,mapaPosiciones[aiAgentName]))
                    return False
            else:
                print ('-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}"'.format(aiBaseName))
                return False
        
        return True
    

