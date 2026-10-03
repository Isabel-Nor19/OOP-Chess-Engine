from abc import ABC, abstractmethod
from Colour import Colour
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Square import Square
    from ChessBoard import ChessBoard



class Piece(ABC):
    """Abstract base class representing a generic chess piece.

    Attributes:
        name (str): Name of the piece.
        colour (Colour): Color enum of the piece.
        captured (bool): Flag tracking if piece has been captured.
        square (Square): Current Square location.
        colour_display (str): ANSI escape code string for terminal rendering.
        symbol_char (str): Single character representing the piece.
    """

    PAWN_COLOUR = "\u001B[33m"     # Yellow
    KNIGHT_COLOUR = "\u001B[32m"   # Green
    BISHOP_COLOUR = "\u001B[35m"   # Purple/Magenta
    Rook_COLOUR = "\u001B[36m"   # Cyan
    QUEEN_COLOUR = "\u001B[95m"    # Bright Magenta
    KING_COLOUR = "\u001B[93m"     # Bright Gold

    def __init__(self, name: str, colour: Colour, square: 'Square', colour_display: str, symbol_char: str = None):
        """Initializes a new Piece instance.

        Args:
            name (str): Name of the piece (e.g., 'Pawn', 'Knight').
            colour (Colour): Color enum of the piece (Colour.WHITE or Colour.BLACK).
            square (Square): Square object where the piece is initially placed.
            colour_display (str): ANSI color escape sequence for terminal output.
            symbol_char (str, optional): Custom character symbol. Defaults to first letter of name.

        Raises:
            TypeError: If colour parameter is not an instance of Colour enum.
        """
        self.name = name

        if not isinstance(colour, Colour):
            raise TypeError(f"colour must be an instance of Colour, got {type(colour)}")

        self.colour = colour
        self.captured = False
        self.square = square
        self.colour_display = colour_display

        char = symbol_char if symbol_char else self.name[0]
        if self.colour == Colour.WHITE:
            self.symbol_char = char.lower()
        else:
            self.symbol_char = char.upper()

    @abstractmethod
    def is_valid_move(self, start_square: 'Square', target_square: 'Square', board: 'ChessBoard') -> bool:
        """Validates if moving from start_square to target_square is legal for this piece.

        Args:
            start_square (Square): The starting square object.
            target_square (Square): The destination square object.
            board (ChessBoard): The chess board instance for checking obstacles and path state.

        Returns:
            bool: True if move is legal according to piece rules, False otherwise.
        """
        pass

    def get_name(self) -> str:
        """Returns the piece's name.

        Returns:
            str: Piece name.
        """
        return self.name

    def get_colour(self) -> Colour:
        """Returns the piece's color enum.

        Returns:
            Colour: Piece color enum.
        """
        return self.colour

    def get_captured(self) -> bool:
        """Returns whether the piece has been captured.

        Returns:
            bool: True if captured, False otherwise.
        """
        return self.captured

    def toggle_captured(self):
        """Toggles the piece's captured status between True and False."""
        self.captured = not self.captured

    def get_square(self) -> 'Square':
        """Returns the Square currently occupied by the piece.

        Returns:
            Square: Occupied square instance.
        """
        return self.square

    def set_square(self, square: 'Square'):
        """Updates the Square occupied by the piece.

        Args:
            square (Square): New target square.
        """
        self.square = square

    def get_colour_display(self) -> str:
        """Returns the ANSI color escape sequence associated with this piece type.

        Returns:
            str: ANSI escape string.
        """
        return self.colour_display 

    def get_symbol_char(self) -> str:
        """Returns the character representation of the piece.

        Returns:
            str: Single character string (lowercase for white, uppercase for black).
        """
        return self.symbol_char

    @abstractmethod
    def get_move_des(self) -> str:
        """Returns a textual description of how this piece moves.

        Returns:
            str: Movement rules description string.
        """
        pass




class Pawn(Piece):
    """Represents a Pawn chess piece."""

    def __init__(self, colour: Colour, square: 'Square', colour_display: str = Piece.PAWN_COLOUR):
        """Initializes a Pawn piece.

        Args:
            colour (Colour): Pawn team color enum.
            square (Square): Target starting square.
            colour_display (str, optional): ANSI sequence. Defaults to Piece.PAWN_COLOUR.
        """
        super().__init__("Pawn", colour, square, Piece.PAWN_COLOUR)

    def get_move_des(self) -> str:
        """Returns movement rule description for Pawns."""
        return "Pawns move forward 1 square (or 2 on their first move)."

    def is_valid_move(self, start_square: 'Square', target_square: 'Square', board: 'ChessBoard') -> bool:
        """Validates forward moves, double initial moves, and diagonal captures for Pawns.

        Args:
            start_square (Square): Starting square.
            target_square (Square): Destination square.
            board (ChessBoard): Board instance.

        Returns:
            bool: True if the pawn move is valid, False otherwise.
        """
        start_row, start_col = start_square.get_row(), start_square.get_col()
        target_row, target_col = target_square.get_row(), target_square.get_col()

        if self.get_colour() == Colour.WHITE:
            direction = -1
            start_row_default = 6
        else:
            direction = 1
            start_row_default = 1

        print('target_row-start_row=', target_row - start_row)
        if target_square.get_occupied_piece() is None:
            # 1. Standard 1-Square Forward Move
            if target_col == start_col and target_row - start_row == direction:
                return True

            # 2. 2-Square Initial Move
            if target_col == start_col and start_row == start_row_default and target_row == start_row + (2 * direction):
                middle_square = board.get_square(start_row + direction, start_col)
                if middle_square.get_occupied_piece() is None:
                    return True 
    
        else:
            if target_row - start_row == direction and target_square.get_occupied_piece().get_colour() != self.get_colour():
                if target_col == start_col + 1 or target_col == start_col - 1:
                    return True
     
        return False


class Knight(Piece):
    """Represents a Knight chess piece."""

    def __init__(self, colour: Colour, square: 'Square', colour_display: str = Piece.KNIGHT_COLOUR):
        """Initializes a Knight piece.

        Args:
            colour (Colour): Knight team color.
            square (Square): Target starting square.
            colour_display (str, optional): ANSI sequence. Defaults to Piece.KNIGHT_COLOUR.
        """
        super().__init__("Knight", colour, square, Piece.KNIGHT_COLOUR, symbol_char="N")

    def get_move_des(self) -> str:
        """Returns movement rule description for Knights."""
        return "Knights move in an 'L' shape. 2 squares in one direction, 1 in another. Not diagonally"

    def is_valid_move(self, start_square: 'Square', target_square: 'Square', board: 'ChessBoard') -> bool:
        """Validates L-shaped jumps for Knights.

        Args:
            start_square (Square): Starting square.
            target_square (Square): Destination square.
            board (ChessBoard): Board instance.

        Returns:
            bool: True if L-shape move is valid, False otherwise.
        """
        start_row, start_col = start_square.get_row(), start_square.get_col()
        target_row, target_col = target_square.get_row(), target_square.get_col()

        if target_square.get_occupied_piece() is None or target_square.get_occupied_piece().get_colour() != start_square.get_occupied_piece().get_colour():
            if abs(target_row - start_row) == 2 and abs(target_col - start_col) == 1:
                return True
            elif abs(target_col - start_col) == 2 and abs(target_row - start_row) == 1:
                return True
      
        return False


class Bishop(Piece):
    """Represents a Bishop chess piece."""

    def __init__(self, colour: Colour, square: 'Square', colour_display: str = Piece.BISHOP_COLOUR):
        """Initializes a Bishop piece.

        Args:
            colour (Colour): Bishop team color.
            square (Square): Target starting square.
            colour_display (str, optional): ANSI sequence. Defaults to Piece.BISHOP_COLOUR.
        """
        super().__init__("Bishop", colour, square, Piece.BISHOP_COLOUR)

    def get_move_des(self) -> str:
        """Returns movement rule description for Bishops."""
        return "Bishops move diagonally, at any length"

    def is_valid_move(self, start_square: 'Square', target_square: 'Square', board: 'ChessBoard') -> bool:
        """Validates diagonal paths for Bishops and checks path clearance.

        Args:
            start_square (Square): Starting square.
            target_square (Square): Destination square.
            board (ChessBoard): Board instance.

        Returns:
            bool: True if diagonal move is valid and unobstructed, False otherwise.
        """
        start_row, start_col = start_square.get_row(), start_square.get_col()
        target_row, target_col = target_square.get_row(), target_square.get_col()
        
        if target_row - start_row > 0: 
            direction_row = 1 
        elif target_row - start_row < 0:
            direction_row = -1

        if target_col - start_col > 0:
            direction_col = 1
        else:
            direction_col = -1

        for s in range(abs(target_row - start_row)):
            step = s + 1
            next_row = start_row + (step * direction_row)
            next_col = start_col + (step * direction_col)
            
            middle_square = board.get_square(next_row, next_col)

            if middle_square.get_space() == target_square.get_space():
                if target_square.get_occupied_piece() is None or target_square.get_occupied_piece().get_colour() != start_square.get_occupied_piece().get_colour():
                    if abs(target_row - start_row) == abs(target_col - start_col):
                        return True
            else:
                if middle_square.get_occupied_piece() is not None:
                    return False


class Rook(Piece):
    """Represents a Rook/Rook chess piece."""

    def __init__(self, colour: Colour, square: 'Square', colour_display: str = Piece.Rook_COLOUR):
        """Initializes a Rook piece.

        Args:
            colour (Colour): Rook team color.
            square (Square): Target starting square.
            colour_display (str, optional): ANSI sequence. Defaults to Piece.Rook_COLOUR.
        """
        super().__init__("Rook", colour, square, Piece.Rook_COLOUR)

    def get_move_des(self) -> str:
        """Returns movement rule description for Rooks/Rooks."""
        return "Rook moves only horizontally and vertically, at any length"

    def is_valid_move(self, start_square: 'Square', target_square: 'Square', board: 'ChessBoard') -> bool:
        """Validates horizontal and vertical paths for Rooks and checks path clearance.

        Args:
            start_square (Square): Starting square.
            target_square (Square): Destination square.
            board (ChessBoard): Board instance.

        Returns:
            bool: True if horizontal/vertical move is valid and unobstructed, False otherwise.
        """
        start_row, start_col = start_square.get_row(), start_square.get_col()
        target_row, target_col = target_square.get_row(), target_square.get_col()

        if target_row - start_row == 0:
            direction_row = 0
            diff = target_col - start_col
            direction_col = 1 if target_col - start_col > 0 else -1
        elif target_col - start_col == 0:
            diff = target_row - start_row
            direction_col = 0
            direction_row = 1 if target_row - start_row > 0 else -1
        else:
            return False

        for s in range(abs(diff)):
            step = s + 1
            next_row = start_row + (step * direction_row)
            next_col = start_col + (step * direction_col)
            
            middle_square = board.get_square(next_row, next_col)

            if middle_square.get_space() == target_square.get_space():
                if target_square.get_occupied_piece() is None or target_square.get_occupied_piece().get_colour() != start_square.get_occupied_piece().get_colour():
                    if target_row == start_row or target_col == start_col:
                        return True               
            else:
                if middle_square.get_occupied_piece() is not None:
                    return False


class King(Piece):
    """Represents a King chess piece."""

    def __init__(self, colour: Colour, square: 'Square', colour_display: str = Piece.KING_COLOUR):
        """Initializes a King piece.

        Args:
            colour (Colour): King team color.
            square (Square): Target starting square.
            colour_display (str, optional): ANSI sequence. Defaults to Piece.KING_COLOUR.
        """
        super().__init__("King", colour, square, Piece.KING_COLOUR)

    def get_move_des(self) -> str:
        """Returns movement rule description for Kings."""
        return "Kings moves 1 square in any direction."

    def is_valid_move(self, start_square: 'Square', target_square: 'Square', board: 'ChessBoard') -> bool:
        """Validates single-square movements in any direction for the King.

        Args:
            start_square (Square): Starting square.
            target_square (Square): Destination square.
            board (ChessBoard): Board instance.

        Returns:
            bool: True if 1-square move is valid, False otherwise.
        """
        start_row, start_col = start_square.get_row(), start_square.get_col()
        target_row, target_col = target_square.get_row(), target_square.get_col()

        if target_square.get_occupied_piece() is None or target_square.get_occupied_piece().get_colour() != start_square.get_occupied_piece().get_colour():
            if abs(target_row - start_row) == 1 or abs(target_col - start_col) == 1:
                if target_row == start_row or target_col == start_col:
                    return True
                elif abs(target_row - start_row) == abs(target_col - start_col):
                    return True
            
        return False


class Queen(Piece):
    """Represents a Queen chess piece."""

    def __init__(self, colour: Colour, square: 'Square', colour_display: str = Piece.QUEEN_COLOUR):
        """Initializes a Queen piece.

        Args:
            colour (Colour): Queen team color.
            square (Square): Target starting square.
            colour_display (str, optional): ANSI sequence. Defaults to Piece.QUEEN_COLOUR.
        """
        super().__init__("Queen", colour, square, Piece.QUEEN_COLOUR)
    
    def get_move_des(self) -> str:
        """Returns movement rule description for Queens."""
        return "Queens moves in any direction, at any length."

    def is_valid_move(self, start_square: 'Square', target_square: 'Square', board: 'ChessBoard') -> bool:
        """Validates linear diagonal, horizontal, and vertical moves for the Queen.

        Args:
            start_square (Square): Starting square.
            target_square (Square): Destination square.
            board (ChessBoard): Board instance.

        Returns:
            bool: True if direction is valid and path is unobstructed, False otherwise.
        """
        start_row, start_col = start_square.get_row(), start_square.get_col()
        target_row, target_col = target_square.get_row(), target_square.get_col()

        if abs(target_row - start_row) == abs(target_col - start_col):
            direction_row = 1 if target_row - start_row > 0 else -1
            direction_col = 1 if target_col - start_col > 0 else -1

            for s in range(abs(target_row - start_row)):
                step = s + 1
                next_row = start_row + (step * direction_row)
                next_col = start_col + (step * direction_col)
                
                middle_square = board.get_square(next_row, next_col)

                if middle_square.get_space() == target_square.get_space():
                    if target_square.get_occupied_piece() is None or target_square.get_occupied_piece().get_colour() != start_square.get_occupied_piece().get_colour():
                        if abs(target_row - start_row) == abs(target_col - start_col):
                            return True
                else:
                    if middle_square.get_occupied_piece() is not None:
                        return False

        elif target_row == start_row or target_col == start_col:        
            if target_row - start_row == 0:
                direction_row = 0
                diff = target_col - start_col
                direction_col = 1 if target_col - start_col > 0 else -1
            elif target_col - start_col == 0:
                diff = target_row - start_row
                direction_col = 0
                direction_row = 1 if target_row - start_row > 0 else -1
            else:
                return False

            for s in range(abs(diff)):
                step = s + 1
                next_row = start_row + (step * direction_row)
                next_col = start_col + (step * direction_col)
                
                middle_square = board.get_square(next_row, next_col)

                if middle_square.get_space() == target_square.get_space():
                    if target_square.get_occupied_piece() is None or target_square.get_occupied_piece().get_colour() != start_square.get_occupied_piece().get_colour():
                        if target_row == start_row or target_col == start_col:
                            return True               
                else:
                    if middle_square.get_occupied_piece() is not None:
                        return False