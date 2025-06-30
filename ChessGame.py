# Enums for piece colors
from enum import Enum

class Color(Enum):
    WHITE = 'WHITE'
    BLACK = 'BLACK'

# ---------------------------
# Basic Classes
# ---------------------------

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.piece = None

    def get_piece(self):
        return self.piece

    def set_piece(self, piece):
        self.piece = piece


class Move:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def from_x(self): return self.source.x
    def from_y(self): return self.source.y
    def to_x(self): return self.target.x
    def to_y(self): return self.target.y


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color


# ---------------------------
# Board
# ---------------------------

class Board:
    def __init__(self):
        self.grid = [[Square(i, j) for j in range(8)] for i in range(8)]

    def get_square(self, x, y):
        return self.grid[x][y]

    def place_piece(self, piece, x, y):
        self.grid[x][y].set_piece(piece)

    def is_valid_move(self, move, player):
        piece = move.source.get_piece()
        return piece and piece.color == player.color and piece.strategy.is_valid(move, self)

    def execute_move(self, move):
        piece = move.source.get_piece()
        move.source.set_piece(None)
        move.target.set_piece(piece)


# ---------------------------
# Strategy Pattern
# ---------------------------

class MoveStrategy:
    def is_valid(self, move, board):
        raise NotImplementedError

class KingMoveStrategy(MoveStrategy):
    def is_valid(self, move, board):
        dx = abs(move.from_x() - move.to_x())
        dy = abs(move.from_y() - move.to_y())
        return dx <= 1 and dy <= 1

class RookMoveStrategy(MoveStrategy):
    def is_valid(self, move, board):
        return move.from_x() == move.to_x() or move.from_y() == move.to_y()


# ---------------------------
# Piece and Factory + Singleton
# ---------------------------

class Piece:
    def __init__(self, color):
        self.color = color
        self.strategy = None

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.strategy = KingMoveStrategy()

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.strategy = RookMoveStrategy()


class PieceFactory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_piece(self, type_name, color):
        type_name = type_name.upper()
        if type_name == "KING": return King(color)
        if type_name == "ROOK": return Rook(color)
        raise ValueError("Unknown piece type: " + type_name)


# ---------------------------
# Observer Pattern
# ---------------------------

class Observer:
    def update(self, event):
        raise NotImplementedError

class Subject:
    def register_observer(self, observer):
        raise NotImplementedError
    def notify_observers(self, event):
        raise NotImplementedError

class GameEvent:
    def __init__(self, source):
        self.source = source

class MoveEvent(GameEvent):
    def __init__(self, source, move):
        super().__init__(source)
        self.move = move


# ---------------------------
# Main Controller
# ---------------------------

class ChessGame(Subject):
    def __init__(self):
        self.board = Board()
        self.observers = []
        self.setup_players()
        self.setup_initial_pieces()

    def setup_players(self):
        self.white = Player("White", Color.WHITE)
        self.black = Player("Black", Color.BLACK)
        self.current = self.white

    def setup_initial_pieces(self):
        factory = PieceFactory()
        self.board.place_piece(factory.create_piece("KING", Color.WHITE), 0, 4)
        self.board.place_piece(factory.create_piece("KING", Color.BLACK), 7, 4)
        self.board.place_piece(factory.create_piece("ROOK", Color.WHITE), 0, 0)
        self.board.place_piece(factory.create_piece("ROOK", Color.BLACK), 7, 0)

    def make_move(self, move):
        if self.board.is_valid_move(move, self.current):
            self.board.execute_move(move)
            self.notify_observers(MoveEvent(self, move))
            self.switch_turn()
        else:
            raise Exception("Invalid move")

    def switch_turn(self):
        self.current = self.black if self.current == self.white else self.white

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, event):
        for o in self.observers:
            o.update(event)


# ---------------------------
# Observer Implementation Example
# ---------------------------

class MoveLogger(Observer):
    def update(self, event):
        if isinstance(event, MoveEvent):
            m = event.move
            print(f"Move: ({m.from_x()}, {m.from_y()}) -> ({m.to_x()}, {m.to_y()})")