# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
from heuristics import *
import random


class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0, len(actions) - 1)]


class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)


class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        root = (state, 0)
        queue = [(root, None)]
        visited = []
        minCost = 10000000
        chooseAction = Directions.STOP
        while len(queue) > 0:
            size = len(queue)
            for i in range(0, size):
                curNode, curAction = queue.pop(0)
                if curNode[0] not in visited:
                    if curNode != root and curNode[1] + admissibleHeuristic(curNode[0]) < minCost:
                        minCost = curNode[1] + admissibleHeuristic(curNode[0])
                        chooseAction = curAction
                    if not curNode[0].isWin() and not curNode[0].isLose():
                        legal = curNode[0].getLegalPacmanActions()
                        successors = [(curNode[0].generatePacmanSuccessor(action), action) for action in legal]
                        for successor in successors:
                            if successor[0] is not None and successor[0] not in visited:
                                queue.append(((successor[0], curNode[1] + 1),
                                              curAction if curAction is not None else successor[1]))
                    visited.append(curNode[0])
        return chooseAction


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP
        root = (state, 0)
        stack = [(root, None)]
        visited = []
        minCost = 10000000
        chooseAction = Directions.STOP
        while len(stack) > 0:
            curNode, curAction = stack.pop()
            if curNode[0] not in visited:
                if curNode != root and curNode[1] + admissibleHeuristic(curNode[0]) < minCost:
                    minCost = curNode[1] + admissibleHeuristic(curNode[0])
                    chooseAction = curAction
                if not curNode[0].isWin() and not curNode[0].isLose():
                    legal = curNode[0].getLegalPacmanActions()
                    successors = [(curNode[0].generatePacmanSuccessor(action), action) for action in legal]
                    for successor in successors:
                        if successor[0] is not None and successor[0] not in visited:
                            stack.append(
                                ((successor[0], curNode[1] + 1), curAction if curAction is not None else successor[1]))
                visited.append(curNode[0])
        return chooseAction


class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        root = (state, 0)
        pq = PriorityQueue()
        pq.put((admissibleHeuristic(state), root, None))
        visited = []
        minCost = 10000000
        chooseAction = Directions.STOP
        while pq.size() > 0:
            (_, curNode, curAction) = pq.get()
            if curNode[0] not in visited:
                if curNode != root and curNode[1] + admissibleHeuristic(curNode[0]) < minCost:
                    minCost = curNode[1] + admissibleHeuristic(curNode[0])
                    chooseAction = curAction
                if not curNode[0].isWin() and not curNode[0].isLose():
                    legal = curNode[0].getLegalPacmanActions()
                    successors = [(curNode[0].generatePacmanSuccessor(action), action) for action in legal]
                    for successor in successors:
                        if successor[0] is not None and successor[0] not in visited:
                            pq.put((curNode[1] + admissibleHeuristic(curNode[0]), (successor[0], curNode[1] + 1),
                                    curAction if curAction is not None else successor[1]))
                visited.append(curNode[0])
        return chooseAction


# class for Priority queue
class PriorityQueue:

    def __init__(self):
        self.queue = list()
        # if you want you can set a maximum size for the queue

    def get(self):
        return self.queue.pop(0)

    def put(self, node):
        # if queue is empty
        if self.size() == 0:
            # add the new node
            self.queue.append(node)
        else:
            # traverse the queue to find the right place for new node
            for x in range(0, self.size()):
                # if the priority of new node is greater
                if node[0] <= self.queue[x][0]:
                    # if we have traversed the complete queue
                    if x == 0:
                        # add new node at the end
                        self.queue.insert(x, node)
                    else:
                        continue
                else:
                    self.queue.insert(x, node)
                    return True

    def size(self):
        return len(self.queue)
