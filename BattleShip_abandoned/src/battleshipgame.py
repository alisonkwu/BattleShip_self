from typing import Iterable, TypeVar
from .board import Board
from .player import Player

# from .ship import Ship
from .ships import Ship

T = TypeVar('T')


class BattleshipGame(object):
    def __init__(self, num_rows: int, num_cols: int, ships, ships2) -> None:
        self.board1 = Board(num_rows, num_cols, ships)
        self.board2 = Board(num_rows, num_cols, ships2)
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.battleShip_orientation = None
        self.ship_orientation_input = None
        self.player1_name = ""
        self.player2_name = ""
        self.player1 = None
        self.player2 = None
        #for player_num in range(2):
           # self.players.append(Player(self.players))
        # self._cur_player_turn = 0
        #self.ships = ships
        #self.board1.ships = ships
        #self.board2.ships = ships
        self.other_player = None
        self.starting_row = None
        self.starting_col = None
        self.player2_life = len(self.board1.ships)
        self.player1_life = len(self.board2.ships)

        self.game_on = True
        self.turn = "Player 1"

    def play(self) -> str:

        # Ask for player 1's name
        self.player1_name = str(input("Player 1 please enter your name: "))
        print(f" {self.player1_name}'s Placement Board" + str(self.board1))  # Print the board for player 1


        self.get_orientation_and_coordinates(self.player1_name, self.board1)

        self.player1 = Player(self.player1_name)  # Create Player 1

        # Ask for player 2's name
        self.player2_name = str(input("Player 2 please enter your name: "))
        while self.player1_name.strip() == self.player2_name.strip():  # Player 2 must have a different name than player 1
            print("Someone is already using " + self.player1_name + " for their name." + "\nPlease choose another name.")
            self.player2_name = str(
                input("Player 2 please enter your name: "))

        #print(self.board1.ships.cells == self.board2.ships.cells)
        print(f"{self.player2_name}'s Placement Board" + str(self.board2))  # Print the board for player 2



        self.get_orientation_and_coordinates(self.player2_name, self.board2)


        self.player2 = Player(self.player2_name)  # Create Player 2

        # Set the boards of the players
        self.player1.create_scanning_board(self.num_rows, self.num_cols, self.board2.ships)
        self.player2.create_scanning_board(self.num_rows, self.num_cols, self.board1.ships)
        self.player1.board = self.board1
        self.player2.board = self.board2

        # GAMEPLAY
        self.turn = self.player1_name # Game starts out with player 1 going first
        while self.game_on:
            if self.turn == self.player1_name: # Player 1's Turn
                # Print the scanning board
                print(self.player1_name + "'s Scanning Board" + str(self.player1.scanning_board))
                #print(self.player1.scanning_board)

                # print the player's board
                print("\n" + self.player1_name + "'s Board" + str(self.player1.board))
                #print(self.player1.board)
            else: # Player 2's Turn
                # Print the scanning board
                print("\n" + self.player2_name + "'s Scanning Board" + str(self.player2.scanning_board))
                #print(self.player2.scanning_board)

                # Print the player's board
                print("\n" +self.player2_name + "'s Board" + str(self.player2.board))
                #print(self.player2.board)

            fire_coordinate = input("\n" + str(self.turn) + ", enter the location you want to fire at in the form row, column:")
            # Get the coordinates of the ship
            coordinates = fire_coordinate.split(",")
            fire_row = coordinates[0].strip()
            fire_col = coordinates[1].strip()

            valid_fire_coordinate = True

            # Check to make sure that the ship's initial coordinates are integers
            if not self.see_coordinates_integers(fire_row, fire_col):
                valid_fire_coordinate = False
            # Check to make sure that the ship's initial coordinate will not be out of bounds
            else:
                if not self.see_coordinates_in_bounds_not_ship(int(fire_row), int(fire_col), int(self.num_rows),int(self.num_cols)):
                    valid_fire_coordinate = False

            while not valid_fire_coordinate:
                fire_coordinate = input(
                    str(self.turn) + ", enter the location you want to fire at in the form row, column:\n")
                # Get the coordinates of the ship
                coordinates = fire_coordinate.split(",")
                fire_row = coordinates[0].strip()
                fire_col = coordinates[1].strip()

                valid_fire_coordinate = True

                # Check to make sure that the ship's initial coordinates are integers
                if not self.see_coordinates_integers(fire_row, fire_col):
                    valid_fire_coordinate = False
                # Check to make sure that the ship's initial coordinate will not be out of bounds
                else:
                    if not self.see_coordinates_in_bounds_not_ship(int(fire_row), int(fire_col), int(self.num_rows),
                                                          int(self.num_cols)):
                        valid_fire_coordinate = False

            # See if the projectile hit a part of the ship
            hit_ship = False
            hit_ship_name = "" # the name of the ship that has been hit
            opponent_name = ""
            if self.turn == self.player1_name:
                opponent_name = self.player2_name
                hit_info = self.player2.board.hit_board(fire_row, fire_col, self.player1)
                #print("hit_info = " + str(hit_info))
                hit_ship = hit_info[0] # whether the ship has been hit or not
                hit_ship_name = hit_info[1]
                ship_died = hit_info[2]

            if self.turn == self.player2_name:
                hit_info = self.player1.board.hit_board(fire_row, fire_col, self.player2)
                #print("hit_info = " + str(hit_info))
                hit_ship = hit_info[0] # whether the ship has been hit or not
                hit_ship_name = hit_info[1]
                ship_died = hit_info[2]
                opponent_name = self.player1_name

            # If the player hit the ship
            if hit_ship:
                print(" You hit " + str(opponent_name) + "'s " + hit_ship_name + "!")
            else: # If the player did not hit the ship
                print(" Miss")

            if ship_died:
                print("You destroyed " + str(opponent_name) + "'s " + hit_ship_name)
                if self.turn == self.player1_name:
                    self.player2_life -= 1
                    if self.player2_life == 0:

                        # Print the scanning board
                        print(self.player1_name + "'s Scanning Board" + str(self.player1.scanning_board))

                        # Print the player's board
                        print("\n" + self.player1_name + "'s Board" + str(self.player1.board))
                        self.turn = self.player1_name

                        return(print("\n" + self.player1_name + " won the game!"))
                        #self.game_on = False

                if self.turn == self.player2_name:
                    self.player1_life -= 1
                    if self.player1_life == 0:

                        # Print the scanning board
                        print(self.player2_name + "'s Scanning Board")
                        print(self.player2.scanning_board)

                        # print the player's board
                        print("\n" + self.player2_name + "'s Board")
                        print(self.player2.board)
                        return(print("\n" + self.player2_name + " won the game!"))
                        #self.game_on = False

            #reprint own boards & switch turns

            if self.turn == self.player1_name:
                # Print the scanning board
                print("\n" + self.player1_name + "'s Scanning Board")
                print(self.player1.scanning_board)

                # print the player's board
                print("\n" + self.player1_name + "'s Board")
                print(self.player1.board)
                self.turn = self.player2_name  # Move to Player 2's Turn
            else:
                # Print the scanning board
                print(self.player2_name + "'s Scanning Board")
                print(self.player2.scanning_board)

                # Print the player's board
                print("\n" +self.player2_name + "'s Board")
                print(self.player2.board)
                self.turn = self.player1_name

        # Ask for the orientation and coordinates of player 2's ships

    # see if a coordinate is a valid number or not

    def coordinate_is_int(self, string:str) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False

    # see if the ship's coordinates are integers
    def see_coordinates_integers(self, row:int, col:int) -> bool:
        coordinates_are_integers = True

        if not self.coordinate_is_int(row):
            print("row: " + str(row) + " is not a valid value for row.\n It should be an integer between 0 and " + str(int(self.num_rows) - 1))
            coordinates_are_integers = False
        if not self.coordinate_is_int(col):
            print("col: " + str(col) + " is not a valid value for column.\n It should be an integer between 0 and " + str(int(self.num_cols) - 1))
            coordinates_are_integers = False

        return coordinates_are_integers

    # see if the ship's coordinates is in bounds
    def see_coordinates_in_bounds(self, row: int, col: int, num_rows : int, num_cols : int, ship) -> bool:
        in_bounds = True

        # check boundary conditions
        if row < 0:
            in_bounds = False
        if row >= num_rows:
            in_bounds = False
        if col < 0:
            in_bounds = False
        if col >= num_cols:
            in_bounds = False

        if not in_bounds:
            print(" Cannot place " + str(ship.ship_name) + " " + str(ship.orientation_input) + " at " + str(row) + ", " + str(
                col) + " because it would be out of bounds.")

        return in_bounds

    # see if the ship's coordinates is in bounds
    def see_coordinates_in_bounds_not_ship(self, row: int, col: int, num_rows : int, num_cols : int) -> bool:
        in_bounds = True

        # check boundary conditions
        if row < 0:
            in_bounds = False
        if row >= num_rows:
            in_bounds = False
        if col < 0:
            in_bounds = False
        if col >= num_cols:
            in_bounds = False

        if not in_bounds:
            print("Cannot fire at " + str(row) + ", " + str(col) + " because it would be out of bounds")

        return in_bounds

    def get_orientation_and_coordinates(self, player_name: str, board: "Board") -> None:
        board_ships = [] # a list of the ships on the board

        # Ask for the orientation and coordinates of player 1's ships
        for i in range(0, len(board.ships)):
            curr_ship = board.ships[i].ship_name  # the name of the current ship we are trying to get information from
            board.ships[i].cells = [] # Reset the cells of the ship
            curr_ship_length = board.ships[
                i].ship_length  # get the length of the current ship we are trying to get information from
            ship_orientation_input = str(input(
                str(player_name) + " enter horizontal or vertical for the orientation of " + curr_ship + " which is "
                + str(curr_ship_length) + " long:"))

            # Keep asking the user for the orientation until its valid
            while True:
                if not "horizontal".startswith(ship_orientation_input.strip().lower()) and not "vertical".startswith(
                        ship_orientation_input.strip().lower()):
                    print(" " + str(ship_orientation_input) + " does not represent an Orientation")
                    ship_orientation_input = str(input(str(
                        player_name + " enter horizontal or vertical for the orientation of " + curr_ship + " which is "
                        + str(curr_ship_length) + " long:")))
                else:
                    self.battleShip_orientation = ship_orientation_input
                    break




            valid_ship_coordinate = False
            while not valid_ship_coordinate:
                # Get the ship's position
                ship_position = str(input(" " +
                    str(player_name) + ", enter the starting position for your " + curr_ship + " ship ,which is " + str(
                        curr_ship_length) + " long, in the form row, column:"))

                # Get the coordinates of the ship
                coordinates = ship_position.split(",")
                starting_row = coordinates[0].strip()
                starting_col = coordinates[1].strip()

                valid_ship_coordinate = True

                # Check to make sure that the ship's initial coordinates are integers
                if not self.see_coordinates_integers(starting_row, starting_col):
                    valid_ship_coordinate = False
                # Check to make sure that the ship's initial coordinate will not be out of bounds
                else:
                    if not self.see_coordinates_in_bounds(int(starting_row), int(starting_col), int(self.num_rows), int(self.num_cols), board.ships[i]):
                        valid_ship_coordinate = False

            if "horizontal".startswith(ship_orientation_input.strip().lower()):
                board.ships[i].orientation = "horizontal"
            if "vertical".startswith(ship_orientation_input.strip().lower()):
                board.ships[i].orientation = "vertical"

            if valid_ship_coordinate:
                #ship = board.ships[i]  # get the current ship

                    # generate the cells that the ship will be placed on
                startingRow = int(starting_row)
                startingCol = int(starting_col)

                # Cells are in the following format: row (int), col (int), hit or not (boolean)
                board.ships[i].cells.append([startingRow, startingCol, False])

                for j in range(0, (board.ships[i].ship_length - 1)):
                    if board.ships[i].orientation == "vertical":
                        board.ships[i].cells.append([startingRow + 1, startingCol, False])
                        startingRow += 1
                    else:
                        board.ships[i].cells.append([startingRow, startingCol + 1, False])
                        startingCol += 1

                #print(self.board1.ships[i].cells == self.board2.ships[i].cells)
                #print(self.board1)
                #print(self.board2)
                #board.place_ship_locations(self.battleShip_orientation, self.starting_row, self.starting_col, board.ships)
                board.place_ship_locations(board.ships)
                print(f" {player_name}'s Placement Board" + str(board))

                #print(board)



