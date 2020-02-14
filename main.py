import sys

from BattleShip.src.battleshipgame import BattleshipGame
from BattleShip.src.ships import Ship

if __name__ == '__main__':
    num_rows = 1
    num_cols = 1
    board = None

    if len(sys.argv) >= 2:  # user provided a board dimension
        path_file = str(sys.argv[1])
        with open(path_file) as f: # opening the file to be read
            line = f.readline()
            line_number = 1
            ships = []
            ships2 = []
            while line: # reading the file line by line
                # process the line
                if line_number == 1:
                    dimension_components = line.split(" ")
                    num_rows = dimension_components[0]
                    num_cols = dimension_components[1]
                else:
                    ship_components = line.split(" ")
                    ship_name = ship_components[0]
                    ship_length = ship_components[1]
                    ships.append(Ship(ship_name, ship_length, "h", 0, 0))
                    ships2.append(Ship(ship_name, ship_length, "h", 0, 0))
                    #print("ship_name = " + str(ship_name) + ", ship_length = " + str(ship_length))

                line = f.readline()
                line_number += 1

            # Create the board
            game = BattleshipGame(num_rows, num_cols, ships, ships2)
            game.play()

    #print(board)
    #game = BattleshipGame(board_dim)
    #game.play()
