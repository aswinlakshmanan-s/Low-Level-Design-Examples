import random
from threading import Thread, Lock
import time

# --- Player Class ---
class Player:
    def __init__(self, name: str):
        self.name = name
        self.position = 1  # All players start from position 1

# --- Dice Class ---
class Dice:
    def __init__(self, faces: int = 6):
        self.faces = faces

    def roll(self) -> int:
        return random.randint(1, self.faces)

# --- Board Class ---
class Board:
    def __init__(self, size: int = 100):
        self.size = size
        self.snakes = {}  # key=head, value=tail
        self.ladders = {} # key=bottom, value=top

    def set_snakes(self, snakes: dict):
        self.snakes = snakes

    def set_ladders(self, ladders: dict):
        self.ladders = ladders

    def get_new_position(self, pos: int) -> int:
        if pos in self.snakes:
            print(f"🐍 Bitten by snake! Slide from {pos} to {self.snakes[pos]}")
            return self.snakes[pos]
        if pos in self.ladders:
            print(f"🪜 Climbed a ladder! Move from {pos} to {self.ladders[pos]}")
            return self.ladders[pos]
        return pos

# --- Game Class ---
class Game:
    def __init__(self, players: list, board: Board):
        self.players = players
        self.board = board
        self.dice = Dice()
        self.winner = None
        self.lock = Lock()

    def start(self):
        print("\n🎮 Starting new game...")
        while not self.winner:
            for player in self.players:
                input(f"\n{player.name}'s turn. Press Enter to roll dice...")
                roll = self.dice.roll()
                print(f"{player.name} rolled a {roll}")
                player.position += roll
                if player.position > self.board.size:
                    player.position = self.board.size  # can't move beyond

                player.position = self.board.get_new_position(player.position)
                print(f"{player.name} is now at {player.position}")

                if player.position == self.board.size:
                    self.winner = player.name
                    print(f"\n🏆 {player.name} has won the game!")
                    return

# --- GameManager Class to Run Multiple Games ---
class GameManager:
    def __init__(self):
        self.games = []

    def create_game(self, player_names: list, snakes: dict, ladders: dict):
        players = [Player(name) for name in player_names]
        board = Board()
        board.set_snakes(snakes)
        board.set_ladders(ladders)
        game = Game(players, board)
        thread = Thread(target=game.start)
        self.games.append(thread)
        thread.start()

# --- Example Run ---
if __name__ == "__main__":
    gm = GameManager()

    # Game 1
    gm.create_game(
        ["Alice", "Bob"],
        snakes={17: 7, 54: 34, 62: 19, 87: 24},
        ladders={3: 22, 5: 8, 20: 29, 70: 90}
    )

    # Game 2 (independent game session)
    gm.create_game(
        ["Charlie", "Diana"],
        snakes={16: 6, 47: 26, 49: 11, 56: 53},
        ladders={2: 23, 9: 31, 25: 44, 40: 80}
    )
