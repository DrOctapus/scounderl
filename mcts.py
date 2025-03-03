from __future__ import annotations
import math
import random

USCB1CONST = 2
random.seed("test")


class Node:
    def __init__(self, state: State, move: Move = None, parent: Node = None, t=0, n=0):
        self.t = t
        self.n = n
        self.children: list[Node] = []
        self.state = state
        self.move = move
        self.parent = parent

    def run(self):
        node = self.getBestChild()
        if node.n <= 10:
            node.rollover()
        else:
            node.expand().rollover()

    def getBestChild(self) -> Node:
        if len(self.children) == 0:
            return self

        max_score = None
        max_child = None
        for child in self.children:
            if child.n == 0:
                return child

            score = child.t / child.n + USCB1CONST * math.sqrt(math.log(self.n) / child.n)
            if max_score == None or score > max_score:
                max_score = score
                max_child = child
        return max_child.getBestChild()

    def expand(self):
        if len(self.children) == 0:
            for state, move in self.state.getMoves():
                self.children.append(Node(state, move, self))

        return random.choice(self.children)

    def rollover(self):
        current_state = self.state.copy()
        while True:
            if current_state.isTerminal():  # TODO: make early stopping
                return self.backpropogate(current_state.getScore())
            current_state, _ = random.choice(current_state.getMoves())  # TODO: make not random

    def backpropogate(self, t):
        self.t += t
        self.n += 1
        if self.parent:
            self.parent.backpropogate(t)
        return t

    def getBestMove(self) -> tuple[State, Move]:
        max_score = None
        max_child = None
        for child in self.children:
            if child.n == 0:
                continue
            score = child.t / child.n
            if max_score == None or score > max_score:
                max_score = score
                max_child = child
        return max_child.state, max_child.move


class State:    
    def getMoves() -> list[tuple[State, Move]]:
        pass

    def getScore() -> int:
        pass

    def copy() -> State:
        pass

    def isTerminal() -> bool:
        pass


class Move:
    pass


def main():
    pass


main()
