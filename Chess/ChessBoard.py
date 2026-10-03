from Colour import Colour
from Square import Square
from Piece import *

RESET = "\u001B[00m"
RED = "\u001B[31m"
WHITE_TEXT = "\u001B[37m"
BLUE_TEXT = "\u001B[34m"


PAWN_COLOR = "\u001B[33m"     # Yellow
KNIGHT_COLOR = "\u001B[32m"   # Green
BISHOP_COLOR = "\u001B[35m"   # Purple/Magenta
ROOK_COLOR = "\u001B[36m"     # Cyan
QUEEN_COLOR = "\u001B[95m"    # Bright Magenta
KING_COLOR = "\u001B[93m"     # Bright Gold

class ChessBoard:
    """Manages the 8x8 chess board, turn rotations, captured pieces, and piece initialization.

    Attributes:
        board (list[list[Square]]): 2D grid matrix of Square objects.
        current_turn (Colour): Active turn team color.
        captured_white (list[Piece]): List of captured white pieces.
        captured_black (list[Piece]): List of captured black pieces.
    """

    def __init__(self):
        """Initializes an 8x8 board grid with alternating black and white Square instances."""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        
        for r in range(0, 8, 1):
            for c in range(0, 8, 1):
                if (r + c) % 2 == 1:
                    self.board[r][c] = Square(r, c, Colour.BLACK, None)
                else:
                    self.board[r][c] = Square(r, c, Colour.WHITE, None)

        self.current_turn = Colour.WHITE
        self.captured_white = []
        self.captured_black = []

    def get_current_turn(self) -> Colour:
        """Returns the color of the active turn player.

        Returns:
            Colour: Active turn color enum.
        """
        return self.current_turn

    def switch_turn(self):
        """Switches current turn between Colour.WHITE and Colour.BLACK."""
        if self.current_turn == Colour.WHITE:
            self.current_turn = Colour.BLACK
        else:
            self.current_turn = Colour.WHITE

    def get_captured_white(self) -> list:
        """Returns list of captured white pieces.

        Returns:
            list[Piece]: Captured white pieces.
        """
        return self.captured_white

    def get_captured_black(self) -> list:
        """Returns list of captured black pieces.

        Returns:
            list[Piece]: Captured black pieces.
        """
        return self.captured_black

    def add_captured_piece(self, captured_piece: Piece):
        """Adds a captured piece to the player's captured list based on team color.

        Args:
            captured_piece (Piece): Piece object captured during gameplay.
        """
        if captured_piece.get_colour() == Colour.WHITE:
            self.captured_white.append(captured_piece)
        else:
            self.captured_black.append(captured_piece)

    def replace_captured_piece(self, chosen_piece: Piece, prawn_piece: Piece):
        """Replaces a chosen captured piece in the captured list during pawn promotion.

        Args:
            chosen_piece (Piece): The captured piece chosen by player to return to board.
            prawn_piece (Piece): The promoted pawn object placed into captured list.
        """
        captured_list = self.captured_white if chosen_piece.get_colour() == Colour.WHITE else self.captured_black
        for p in range(0, len(captured_list), 1):
            if captured_list[p] == chosen_piece:
                captured_list[p] = prawn_piece
                break

    def get_square(self, row: int, col: int) -> Square:
        """Retrieves the Square object located at specified row and column.

        Args:
            row (int): Row coordinate (0-7).
            col (int): Column coordinate (0-7).

        Returns:
            Square: Target square instance.
        """
        return self.board[row][col]

    def initialize_pieces(self):
        """Populates the chess board with default starting pieces for both players."""
        for c in range(0, 8, 1):
            P = Pawn(Colour.BLACK, self.get_square(1, c))
            self.get_square(1, c).occupied_piece = P
            
            p = Pawn(Colour.WHITE, self.get_square(6, c))
            self.get_square(6, c).occupied_piece = p

            if c == 0 or c == 7:
                Piece_Type = Rook
            elif c == 1 or c == 6:
                Piece_Type = Knight
            elif c == 2 or c == 5:
                Piece_Type = Bishop
            elif c == 3:
                Piece_Type = Queen
            elif c == 4:
                Piece_Type = King

            T_B = Piece_Type(Colour.BLACK, self.get_square(0, c))
            self.get_square(0, c).occupied_piece = T_B
            
            T_W = Piece_Type(Colour.WHITE, self.get_square(7, c))
            self.get_square(7, c).occupied_piece = T_W

    def chess_board(self) -> str:
        """Generates ANSI-formatted text representation of the current board state.

        Returns:
            str: Multi-line string showing board and piece codes.
        """
        sb = []
        for r in range(0, 8, 1):
            for c in range(0, 8, 1):
                square = self.board[r][c]
                piece = square.get_occupied_piece()

                if piece is not None:
                    sb.append(f"{piece.get_colour_display()}{piece.get_symbol_char()}{piece.get_colour_display()}")
                else:
                    color_name = square.get_square_colour().name[0]
                    if color_name == "W":
                        sb.append(f"{self.WHITE_TEXT}w{self.RESET}")
                    else:
                        sb.append(f"{self.BLUE_TEXT}B{self.RESET}")
                sb.append("  ")

            sb.append("  ")
            sb.append(f"{self.RED}{r} {self.RESET}")
            sb.append("\n")

        sb.append(f"{self.RED}0  1  2  3  4  5  6  7\n{self.RESET}")
            
        return "".join(sb)