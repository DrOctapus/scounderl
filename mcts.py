from __future__ import annotations
import math
import random

USCB1CONST = 2
# random.seed("test")


class Node:
    def __init__(self, state: State, move: Move = None, parent: Node = None, t=0, n=0):
        self.t = t
        self.n = n
        self.children: list[Node] = []
        self.state = state
        self.move = move
        self.parent = parent

    def run(self, reps):
        for _ in range(reps):
            node = self.getBestChild()
            if node.n <= 15:
                node.rollover()
            else:
                node.expand().rollover()

        return self.getBestMove()

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
        if self.state.isTerminal():
            return self
        
        if len(self.children) == 0:
            for state, move in self.state.getMoves():
                self.children.append(Node(state, move, self))

        return random.choice(self.children)

    def rollover(self):
        current_state = self.state.copy()
        while not current_state.isTerminal():  # TODO early stopping
            if current_state.player == 1:
                current_state, _ = random.choice(current_state.getMoves())  # TODO make not random
            else:
                current_state.simulate()

        return self.backpropagate(current_state.getScore())

    def backpropagate(self, t):
        self.t += t
        self.n += 1
        if self.parent:
            self.parent.backpropagate(t)
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
        if not max_child:
            return None
        return max_child.state, max_child.move

    def __str__(self):
        return f"{self.t} / {self.n}"


class State:
    def __init__(self, board: list[list[int]] = None, player: int = 1):
        if board:
            self.board = board
        else:
            board = []
            for i in range(3):
                board.append([0, 0, 0])
            self.board = board
        self.player = player

    def getMoves(self) -> list[tuple[State, Move]]:
        if self.player == -1:
            print("MOVE ERROR")
            self.simulate()

        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    new_state = self.copy()
                    new_state.board[i][j] = 1
                    new_state.player = -1
                    moves.append((new_state, Move(i, j)))
        return moves

    def simulate(self):
        if self.player == 1:
            print("SIMULATE ERROR")
            return None
        self.player = 1

        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    moves.append((i, j))

        move = random.choice(moves)
        self.board[move[0]][move[1]] = -1

    def getScore(self) -> int:
        for line in self.getWinningLines():
            if line == [1, 1, 1]:
                return 1
            if line == [-1, -1, -1]:
                return -1
        return 0

    def getWinningLines(self):
        """Returns all possible winning lines (rows, cols, diagonals)."""
        return self.board + list(map(list, zip(*self.board))) + [[self.board[i][i] for i in range(3)], [self.board[i][2 - i] for i in range(3)]]  # Rows  # Columns  # Main diagonal  # Anti-diagonal

    def copy(self) -> State:
        return State([row[:] for row in self.board], self.player)

    def isTerminal(self) -> bool:
        terminal = self.getScore() != 0
        if terminal:
            return terminal
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return False
        return True

    def __str__(self):
        symbols = {1: "X", -1: "O", 0: " "}
        return "\n".join([" | ".join(symbols[cell] for cell in row) for row in self.board]) + "\n"


# class State:
#     def getMoves(self) -> list[tuple[State, Move]]:
#         pass

#     def getScore(self) -> int:
#         pass

#     def copy(self) -> State:
#         pass

#     def isTerminal(self) -> bool:
#         pass

#     def simulate(self):
#         pass


class Move:
    def __init__(self, i: int, j: int):
        self.move = (i, j)


def main():
    node = Node(State(player=-1))
    print(node.state)
    while not node.state.isTerminal():
        state, move = node.run(100)
        node = Node(state, move)
        print(node.state)


main()
