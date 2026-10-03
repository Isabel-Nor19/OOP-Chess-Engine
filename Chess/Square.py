from Colour import Colour
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Piece import Piece

class Square:
    """Represents an individual square on the chess board.

    Attributes:
        row (int): The row index on the board (0-7).
        col (int): The column index on the board (0-7).
        square_colour (Colour): The background color of the square.
        occupied_piece (Piece | None): The chess piece occupying this square, if any.
    """

    def __init__(self, row: int, col: int, square_colour: Colour, occupied_piece: 'Piece' = None):
        """Initializes a Square instance with coordinates, color, and optional piece.

        Args:
            row (int): The row index (0-7).
            col (int): The column index (0-7).
            square_colour (Colour): Background color enum of the square.
            occupied_piece (Piece, optional): Initial piece occupying the square. Defaults to None.

        Raises:
            ValueError: If row or col fall outside the valid board range (0-7).
        """
        if 0 <= row < 8 and 0 <= col < 8:
            self.row = row
            self.col = col
        else:
            raise ValueError("Coordinates must be between 0 and 7")
        self.square_colour = square_colour
        self.occupied_piece = occupied_piece

    def get_row(self) -> int:
        """Returns the row index of the square.

        Returns:
            int: The row index (0-7).
        """
        return self.row

    def get_col(self) -> int:
        """Returns the column index of the square.

        Returns:
            int: The column index (0-7).
        """
        return self.col

    def get_space(self) -> str:
        """Returns the string representation of coordinates.

        Returns:
            str: String in '(row,col)' format.
        """
        return f"({self.row},{self.col})"

    def get_occupied_piece(self) -> 'Piece':
        """Returns the piece currently occupying the square.

        Returns:
            Piece | None: Occupying piece or None if square is empty.
        """
        return self.occupied_piece

    def set_occupied_piece(self, playing_piece: 'Piece'):
        """Sets or updates the piece occupying this square.

        Args:
            playing_piece (Piece | None): The new piece occupying the square.
        """
        self.occupied_piece = playing_piece 

    def get_square_colour(self) -> Colour:
        """Returns the color enum of the square.

        Returns:
            Colour: The Colour enum (BLACK or WHITE).
        """
        return self.square_colour

    def __str__(self) -> str:
        """Returns a string description of the square state.

        Returns:
            str: Descriptive string detailing coordinates and occupant.
        """
        return f"Square [row={self.row}, col={self.col}, SquareColour={self.square_colour}, occupiedPiece={self.occupied_piece}]"