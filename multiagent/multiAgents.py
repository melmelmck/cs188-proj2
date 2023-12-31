# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        distances = []
        for food in newFood.asList():
            distances.append(manhattanDistance(newPos, food))

        if distances:
            minDist = min(distances)
        else:
            minDist = 0
        
        return successorGameState.getScore() + (1 / (minDist + 1))

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        legalActions = gameState.getLegalActions(0)
        bestValue = -float('inf')
        bestActionIndex = None
        currDepth = 0
        successors = [gameState.generateSuccessor(0, action) for action in legalActions]
        for i in range(len(successors)):
            currValue = self.value(successors[i], 1, currDepth)
            if currValue > bestValue:
                bestValue = currValue
                bestActionIndex = i
        return legalActions[bestActionIndex]

    def value(self, gameState, agentIndex, currDepth):
        # if the state is terminal, return state's utility
        if gameState.isWin() or gameState.isLose() or self.depth == currDepth:
            return self.evaluationFunction(gameState)
        # if the next agent is max, return max-value(state)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, currDepth)
        # if the next agent is min, return min-value(state)
        if agentIndex > 0:
            return self.minValue(gameState, agentIndex, currDepth)
        
    def maxValue(self, gameState, agentIndex, currDepth):
        v = -float('inf')
        actions = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in actions]
        for successor in successors:
            v = max(v, self.value(successor, agentIndex + 1, currDepth))
        return v
    
    def minValue(self, gameState, agentIndex, currDepth):
        v = float('inf')
        actions = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in actions]
        for successor in successors:
            if (agentIndex + 1) == gameState.getNumAgents():
                currDepth += 1
                agentIndex = -1
            v = min(v, self.value(successor, agentIndex + 1, currDepth))
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        legalActions = gameState.getLegalActions(0)
        bestValue = -float('inf')
        bestActionIndex = None
        currDepth = 0
        alpha = -float('inf')
        beta = float('inf')
        successors = [gameState.generateSuccessor(0, action) for action in legalActions]
        for i in range(len(successors)):
            currValue = self.value(successors[i], 1, currDepth, alpha, beta)
            if currValue > bestValue:
                bestValue = currValue
                bestActionIndex = i
            if bestValue > beta:
                return legalActions[bestActionIndex]
            alpha = max(alpha, bestValue)
        return legalActions[bestActionIndex]
    
    def value(self, gameState, agentIndex, currDepth, alpha, beta):
        # if the state is terminal, return state's utility
        if gameState.isWin() or gameState.isLose() or self.depth == currDepth:
            return self.evaluationFunction(gameState)
        # if the next agent is max, return max-value(state)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, currDepth, alpha, beta)
        # if the next agent is min, return min-value(state)
        if agentIndex > 0:
            return self.minValue(gameState, agentIndex, currDepth, alpha, beta)
        
    def maxValue(self, gameState, agentIndex, currDepth, alpha, beta):
        v = -float('inf')
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            v = max(v, self.value(successor, agentIndex + 1, currDepth, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v
    
    def minValue(self, gameState, agentIndex, currDepth, alpha, beta):
        v = float('inf')
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            if (agentIndex + 1) == gameState.getNumAgents():
                currDepth += 1
                agentIndex = -1
            v = min(v, self.value(successor, agentIndex + 1, currDepth, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        legalActions = gameState.getLegalActions(0)
        bestValue = -float('inf')
        bestActionIndex = None
        currDepth = 0
        successors = [gameState.generateSuccessor(0, action) for action in legalActions]
        for i in range(len(successors)):
            currValue = self.value(successors[i], 1, currDepth)
            if currValue > bestValue:
                bestValue = currValue
                bestActionIndex = i
        return legalActions[bestActionIndex]
    
    def value(self, gameState, agentIndex, currDepth):
        # if the state is terminal, return state's utility
        if gameState.isWin() or gameState.isLose() or self.depth == currDepth:
            return self.evaluationFunction(gameState)
        # if the next agent is max, return max-value(state)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, currDepth)
        # if the next agent is min, return min-value(state)
        if agentIndex > 0:
            return self.expValue(gameState, agentIndex, currDepth)
        
    def maxValue(self, gameState, agentIndex, currDepth):
        v = -float('inf')
        actions = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in actions]
        for successor in successors:
            v = max(v, self.value(successor, agentIndex + 1, currDepth))
        return v
    
    def expValue(self, gameState, agentIndex, currDepth):
        v = 0
        actions = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in actions]
        next_ind = agentIndex + 1
        for successor in successors:
            if next_ind == gameState.getNumAgents():
                currDepth += 1
                next_ind = 0
            p = 1/(len(actions))
            v += p * self.value(successor, next_ind, currDepth)
        return v

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Linear combination of the current game state's score, the distance away from the closest fruit, 
    how far away the ghosts are, and if the ghosts are stunned. How much food is remaining. 
    """
    newFood = currentGameState.getFood()
    newPos = currentGameState.getPacmanPosition()
    newGhostPos = currentGameState.getGhostPositions()
    newGhostStates = currentGameState.getGhostStates()
    eval = 0
    dist = []
    # calculate the distance away from the closest fruit
    for food in newFood.asList():
        dist.append(util.manhattanDistance(food, newPos))
    if (len(dist) != 0):
        eval += 1/min(dist)

    # calculate how much food is remaining
    if (len(newFood.asList()) != 0):
        eval += 1/len(newFood.asList()) 

    # calculate how far away the ghosts are
    distGhost = []
    for ghost in newGhostPos:
        distGhost.append(util.manhattanDistance(ghost, newPos))
    if (len(distGhost) != 0):
        if (min(distGhost) < 2 and min(distGhost) != 0):
            eval += 1/min(distGhost)

    # ghosts stunned timer list
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    if (len(newScaredTimes) != 0 and max(newScaredTimes) != 0):
        eval += 1/max(newScaredTimes)

    return eval + (currentGameState.getScore() * 0.6)

# Abbreviation
better = betterEvaluationFunction
