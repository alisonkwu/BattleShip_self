from .ships import Ship
from typing import List

class Board(object):

    def __init__(self, rows: int, cols: int, ships: List["Ship"]) -> None:

        self.row_count = int(rows)
        self.col_count = int(cols)

        # Stores a list of Ships (Ship objects) on the board
        self.cell = None # Cells are in the following format: row (int), col (int), hit or not (boolean)
        self.board_display = []
        self.ships = ships

        # Construct the board display
        for r in range(0, self.row_count):
            row = []
            for c in range(0, self.col_count):
                row.append("*")
            self.board_display.append(row)

    # checks that a position on the board was hit and returns whether the ship has been hit and the ship name
    def hit_board(self, row : int, col : int, player: "Player") -> List:
        hit_ship = False
        dead_ship = False
        ship_name = ""
        # Go through all the ships
        for ship in self.ships:
            # Go through all the cells in the ship
            for cell in ship.cells:
                # Check that the cell matches the projectile row and column and that that cell has not already been hit
                if int(row) == int(cell[0]) and int(col) == int(cell[1]) and not cell[2]:
                    hit_ship = True
                    # Mark the cell as hit
                    cell[2] = True

                    ship.health -= 1
                    if ship.health == 0:
                        dead_ship = True
                    ship_name = ship.ship_name

                    # Mark the scanning board of the player that fired the projectile with an X = hit
                    player.scanning_board.board_display[int(row)][int(col)] = "X"
                    self.board_display[int(row)][int(col)] = "X"
                # Mark the scanning board of the player that fired the projectile with an O = miss
        if hit_ship == False:
            #if int(row) != int(cell[0]) and int(col) == int(cell[1]) and not cell[2]:
                player.scanning_board.board_display[int(row)][int(col)] = "O"
                self.board_display[int(row)][int(col)] = "O"

        return [hit_ship, ship_name, dead_ship]




    def __str__(self) -> str:
        initial_spacing = max(len(str(self.col_count - 1)), len(str(self.col_count - 1)))
        spacing = " " * initial_spacing
        return_string = ""

        for r in range(0, self.row_count + 1):
            if r == 0:  # First row
                first_row = " " * (initial_spacing + 1)
                for c in range(0, self.col_count):
                    spacing = " " * (initial_spacing - (len(str(c)) - 1))
                    first_row += str(c)
                    if c < self.col_count -1:
                        first_row += spacing
                return_string += "\n" + first_row + "\n"
            else:  # Other rows
                row_list = []
                string_row_list = ""
                other_row = str((r - 1))
                spacing = " " * (initial_spacing - (len(str(r - 1)) - 1))
                for c in range(0, self.col_count):
                    row_list.append(spacing + self.board_display[r - 1][c])
                for i in range(len(row_list)):
                    string_row_list += row_list[i]
                return_string += (other_row + string_row_list)
                #board_display_list.append(row_list)
                if r < self.row_count:
                    return_string += "\n"

        # need to be able to refer to the *
        # store where ships are, change coordinate.
        # loop thru all ships,

        return return_string



    def place_ship_locations(self, ships: List["Ship"]) -> None: # pass in a battleShip object to
        # go through the list of ships

        for i in range(0, len(ships)):

            # go through the cells in the ships
            for j in range(0, len(ships[i].cells)):
                self.board_display[ships[i].cells[j][0]][ships[i].cells[j][1]] = ships[i].ship_name[0]

        
             
       # if "vertical".startswith(ship_orientation.strip()):
        

