from typing import Iterable, List
#from .ship import Ship

#opponent....
from BattleShip.src.board import Board


class Player(object):
    def __init__(self, name : str) -> None:
        self.name = name
        self.scanning_board = None # Stores the board recording hits the user has made
        self.board = None # Stores the board recording the user's ships
        self.alive = True # Player is dead when all the ships are destroyed

    def create_scanning_board(self, row : int, col : int, ships: List["Ship"]) -> Board:
        self.scanning_board = Board(row, col, ships)

    @staticmethod
    def get_name_from_player(self, other_players: Iterable["Player"]) -> str:
        already_used_names = set([player.name for player in other_players])
        while True:
            name = input("Please enter your name: ")
            if name not in already_used_names:
                return name
            else:
                print(f'{name} has already been used. Pick another name.')

    def __str__(self) -> str:
        return self.name