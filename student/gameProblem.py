#
'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''

import simpleai.search
from simpleai.search import SearchProblem, astar

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

        # current state information
        actions = []
        pos = state[0]
        battery = state[2]

        # potential moves
        pos_east = (pos[0]+1, pos[1])
        pos_west = (pos[0]-1, pos[1])
        pos_north = (pos[0], pos[1]-1)
        pos_south = (pos[0], pos[1]+1)
        
        # append to action list if valid move
        if self.can_fly(pos_east) and battery >= self.getAttribute(pos_east, "cost"):
            actions.append('East')
        if self.can_fly(pos_west) and battery >= self.getAttribute(pos_west, "cost"):
            actions.append('West')
        if self.can_fly(pos_north) and battery >= self.getAttribute(pos_north, "cost"):
            actions.append('North')
        if self.can_fly(pos_south) and battery >= self.getAttribute(pos_south, "cost"):
            actions.append('South')
      
        return actions
    
    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''
        pos = state[0]
        goals_left = state[1]
        battery = state[2]

        # update position
        if action is "East":
            new_position = (pos[0]+1, pos[1])
        elif action is "West":
            new_position = (pos[0]-1, pos[1])
        elif action is "North":
            new_position = (pos[0], pos[1]-1)
        elif action is "South":
            new_position = (pos[0], pos[1]+1)

        #update battery
        new_battery = battery - self.getAttribute(new_position, "cost")
        if tuple(self.CONFIG.get("station")) == new_position:
            new_battery = self.CONFIG.get("capacity")

        # if at goal, update goal set
        if new_position in goals_left:
            s = set()
            s.add(new_position)
            goals_left -= frozenset(s)

        return (new_position, goals_left, new_battery)

    def is_goal(self, state):
        '''Returns true if state is the final state (ignores battery)
        '''     
        return state[0] == self.GOAL[0] and state[1] == self.GOAL[1]

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        cost = self.getAttribute(state2[0], "cost") 
        if cost is not None:
            return cost
        return sys.maxsize

    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''
        current = state[0]
        goals_left = state[1]
        
        # gives priority to paths with fewer goals, based on this weighting
        MULTIPLIER = 5
        
        if len(goals_left) > 0:
            goal_distances = set()

            for location in goals_left:
                goal_distances.add(self.dist(current, location))

            return min(goal_distances) + (MULTIPLIER * len(goals_left))
        else:
            return self.dist(current, self.AGENT_START)

    def setup (self):

        base = self.AGENT_START
        goals = frozenset(self.POSITIONS.get("goal"))
        battery = self.CONFIG.get("capacity")

        initial_state = (base, goals, battery)
        final_state = (base, frozenset(), 0)
        algorithm = astar   
        
        return initial_state,final_state,algorithm

    # --------------- Helper Methods  ----------------- #
    
    def can_fly(self, position):
        if 0 <= position[0] < len(self.MAP) and 0 <= position[1] < len(self.MAP[0]):  
            return self.MAP[position[0]][position[1]][2].get('blocked') is not True
        return False

    def dist(self, start, end):
        sx, sy = start
        ex, ey = end
        return abs(ex - sx) + abs(ey - sy)
    
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
        print(self.CONFIG.get("map_size"))
        print(position)
        print([position[1]])
        print(self.MAP[position[0]][position[1]])
        tileAttributes=self.MAP[position[0]][position[1]][2]
        if attributeName in tileAttributes.keys():
            return tileAttributes[attributeName]
        else:
            return None
        
    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
    def initializeProblem(self,map,positions,conf,aiBaseName):

        # Loads the problem attributes: self.AGENT_START, self.POSITIONS,etc.
        if self.mapInitialization(map,positions,conf,aiBaseName):
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
    

