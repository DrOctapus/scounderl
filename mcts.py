from __future__ import annotations
import math

USCB1CONST = 2


class Node:
    def __init__(self, state: State, move: Move = None, t=0, n=0):
        self.t = t
        self.n = n
        self.children: list[Node] = []
        self.state = state
        self.move = move

    def run(self):
        node = self.getBestChild()
        if node.n == 0:
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
                max_child = child
                break
            
            score = child.t / child.n + USCB1CONST * math.sqrt(math.log(self.n) / child.n)
            if max_score == None or score > max_score:
                max_score = score
                max_child = child
        return max_child.getBestChild()

    def expand(self):
        for state, move in self.state.getMoves():
            self.children.append(Node(state, move))
        return self.children[0]

    def rollover(self):
        pass

    def getBestMove(self) -> tuple[State, Move]:
        max_score = None
        max_child = None
        for child in self.children:
            if child.t == 0:
                continue
            score = child.n / child.t
            if max_score == None or score > max_score:
                max_score = score
                max_child = child
        return max_child.state, max_child.move


class State:
    def getMoves() -> list[tuple[State, Move]]:
        pass
    
    def getScore() -> int:
        pass


class Move:
    pass


def main():
    pass


main()
