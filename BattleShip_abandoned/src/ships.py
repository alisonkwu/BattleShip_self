class Ship(object):
    def __init__(self, name: str, length: int, orientation: str, row: int, col: int) -> None:
        self.ship_name = name
        self.ship_length = int(length)
        self.row = row
        self.col = col
        self.piece = None
        self.cells = [] # Array of the cells the ship occupies
        self.health = int(length)

        self.orientation = ""

    #def get_ship_length(self):
        #return self.ship_length

    #def create_piece(self):
        #self.piece = self.ship_name[0] #first letter of Ship Name

    #def health(self) -> int:
        #self.health = self.ship_length
   # def health_loss(self):
        #if player hits one of the self.piece, lose health

    """
    def dead(self):
        if self.health == 0:
            return True

    def cells(self): """


