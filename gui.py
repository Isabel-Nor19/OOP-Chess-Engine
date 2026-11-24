import sys
import pygame
from ChessBoard import ChessBoard
from Colour import Colour
from Piece import Pawn, Piece

# Screen & Board Setup
BOARD_SIZE = 800 #640
SQUARE_SIZE = BOARD_SIZE // 8
SIDEBAR_WIDTH = 200
FPS = 45

# Colour Palette (RGB)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
WHITE_PIECE = (255, 255, 255)
BLACK_PIECE = (20, 20, 20)
SELECTED_SQUARE_COLOR = (0, 100, 0, 160)
VALID_MOVE_COLOR = (120, 220, 150, 130)

# Selected state tracking
selected_square = None  # Stores the starting Square object
captured_rects = []
# Dictionary to hold transformed Pygame Surface objects
PIECE_IMAGES = {}

# Game States
MENU = "MENU"
PLAYING = "PLAYING"
PAUSED = "PAUSED"

game_state = MENU


def draw_start_menu(screen: pygame.Surface) -> pygame.Rect:
    """Renders the main start menu screen and start button.

    Args:
        screen (pygame.Surface): The Pygame display surface to draw onto.

    Returns:
        pygame.Rect: The clickable rectangular region of the Start button.
    """
    screen.fill((30, 30, 30)) 
    
    
    title_text = font.render("CHESS GAME", True, (255, 255, 255))
    screen.blit(title_text, (BOARD_SIZE // 2 - 100, 150))
    
    
    start_btn = pygame.Rect(BOARD_SIZE // 2 - 100, 300, 200, 60)
    pygame.draw.rect(screen, (0, 150, 0), start_btn)
    
    btn_text = font.render("START", True, (255, 255, 255))
    screen.blit(btn_text, (BOARD_SIZE // 2 - 60, 310))
    
    return start_btn


def draw_pause_menu(screen: pygame.Surface) -> pygame.Rect:
    """Renders the pause menu overlay and resume button.

    Args:
        screen (pygame.Surface): The Pygame display surface to draw onto.

    Returns:
        pygame.Rect: The clickable rectangular region of the Resume button.
    """
    overlay = pygame.Surface((BOARD_SIZE + SIDEBAR_WIDTH, BOARD_SIZE))
    overlay.fill((30, 30, 30))
    screen.blit(overlay, (0, 0))

    resume_btn = pygame.Rect(BOARD_SIZE // 2 - 100, 300, 300, 60)
    pygame.draw.rect(screen, (0, 150, 0), resume_btn)
    
    btn_text = font.render("RESUME", True, (255, 255, 255))
    screen.blit(btn_text, (BOARD_SIZE // 2 - 60, 310))
    
    return resume_btn


def load_piece_images():
    """Loads SVG piece assets from disk and scales them to fit square dimensions."""
    pieces = ['P', 'N', 'B', 'R', 'Q', 'K']
    colors = ['b', 'w']  # w = White, b = Black
    
    for color in colors:
        for piece in pieces:
            filename = f"Assets/{color}{piece}.svg"  
            
            image = pygame.image.load(filename)
            PIECE_IMAGES[f"{color}{piece}"] = pygame.transform.smoothscale(
                image, (SQUARE_SIZE, SQUARE_SIZE)
            )


def draw_captured_pieces(screen: pygame.Surface, board: ChessBoard):
    """Renders captured white and black pieces on the right sidebar panel.

    Args:
        screen (pygame.Surface): The Pygame display surface to draw onto.
        board (ChessBoard): The chess board instance containing captured piece lists.
    """
    global captured_rects
    captured_rects.clear()

    siedebar_rect = pygame.Rect(BOARD_SIZE, 0, SIDEBAR_WIDTH, BOARD_SIZE)
    pygame.draw.rect(screen, (50, 50, 50), siedebar_rect)

    x_white = BOARD_SIZE + 10
    x_black = BOARD_SIZE + 100
    y = 10

    for i, piece in enumerate(board.captured_white):
        symbol = piece.get_symbol_char().upper()
        text_colour = 'w' 
        key = f"{text_colour}{symbol}"
        image = PIECE_IMAGES[key]

        pos_y = y + (i * 80)
        piece_rect = pygame.Rect(x_white, pos_y, SQUARE_SIZE, SQUARE_SIZE)
        screen.blit(image, (x_white, pos_y))
        captured_rects.append((piece_rect, piece))

    for i, piece in enumerate(board.captured_black):
        symbol = piece.get_symbol_char().upper()
        text_colour = 'b' 
        key = f"{text_colour}{symbol}"
        image = PIECE_IMAGES[key]

        pos_y = y + (i * 80)
        piece_rect = pygame.Rect(x_black, pos_y, SQUARE_SIZE, SQUARE_SIZE)
        screen.blit(image, (x_black, pos_y))
        captured_rects.append((piece_rect, piece))


# Initialize Pygame & Screen
pygame.init()
load_piece_images()
screen = pygame.display.set_mode((BOARD_SIZE + SIDEBAR_WIDTH, BOARD_SIZE))
pygame.display.set_caption("Python Chess")
font = pygame.font.SysFont("Arial", 42, bold=True)
clock = pygame.time.Clock()

# Initialize Backend Game Engine
board = ChessBoard()
board.initialize_pieces()


def draw_board(screen: pygame.Surface):
    """Renders the 8x8 grid and highlights the selected square and the valid target moves.

    Args:
        screen (pygame.Surface): The Pygame display surface to draw onto.
    """
    for r in range(8):
        for c in range(8):
            sq = board.get_square(r, c)
            
            if sq.get_square_colour() == Colour.WHITE:
                colour = LIGHT_SQUARE 
            else:
                colour = DARK_SQUARE

            rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, colour, rect)

            # Highlight selected square and target squares
            if selected_square:
                if selected_square.get_col() == c and selected_square.get_row() == r:
                    pygame.draw.rect(screen, SELECTED_SQUARE_COLOR, rect)
                # 2. ADD THIS: Fill all valid target squares solid
                else:
                    moving_piece = selected_square.get_occupied_piece()
                    if moving_piece.is_valid_move(selected_square, sq, board):
                        pygame.draw.rect(screen, VALID_MOVE_COLOR, rect)



def draw_pieces(screen: pygame.Surface, board: ChessBoard):
    """Renders piece images onto their respective occupied squares.

    Args:
        screen (pygame.Surface): The Pygame display surface to draw onto.
        board (ChessBoard): The chess board instance containing square occupancy state.
    """
    for r in range(8):
        for c in range(8):
            sq = board.get_square(r, c)
            piece = sq.get_occupied_piece()

            if isinstance(piece, Piece) and piece.get_captured() == False:
                symbol = piece.get_symbol_char().upper()
                text_colour = 'w' if piece.get_colour() == Colour.WHITE else 'b'
                key = f"{text_colour}{symbol}"
                image = PIECE_IMAGES[key]

                pixel_x = c * SQUARE_SIZE
                pixel_y = r * SQUARE_SIZE

                screen.blit(image, (pixel_x, pixel_y))


promotion_pawn_square = None
running = True

while running == True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Toggle Pause with ESC key during gameplay
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # print("escape button clicked")
                if game_state == PLAYING:
                    game_state = PAUSED
                elif game_state == PAUSED:
                    game_state = PLAYING

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if game_state == MENU:
                if start_btn_rect.collidepoint(mouse_x, mouse_y):
                    game_state = PLAYING

            
            elif game_state == PAUSED:
                if resume_btn_rect.collidepoint(mouse_x, mouse_y):
                    game_state = PLAYING

            elif game_state == PLAYING:
                
                # print(promotion_pawn_square)
                if promotion_pawn_square is not None and len(board.get_captured_white()) != 0 and len(board.get_captured_black()) != 0 :
                    prawn_piece = promotion_pawn_square.get_occupied_piece()
                    for rect, chosen_piece in captured_rects:
                        if rect.collidepoint(mouse_x, mouse_y):
                            # Ensure player picks a captured piece matching their color
                            if chosen_piece.get_colour() == prawn_piece.get_colour():
                                # Swap pawn on board with chosen piece
                                promotion_pawn_square.set_occupied_piece(chosen_piece)
                                chosen_piece.set_square(promotion_pawn_square)

                                # Remove piece from backend captured list
                                board.replace_captured_piece(chosen_piece, prawn_piece)

                                # Resume normal play and pass turn
                                promotion_pawn_square = None
                                board.switch_turn()
                                break
                else:
                    if mouse_x < BOARD_SIZE:
                        col = mouse_x // SQUARE_SIZE
                        row = mouse_y // SQUARE_SIZE
                        clicked_square = board.get_square(row, col)
                    
                        if selected_square is None:
                            # First Click: Select a piece of your team
                            if clicked_square.get_occupied_piece() is not None and clicked_square.get_occupied_piece().get_colour() == board.get_current_turn():
                                selected_square = clicked_square
                                # for target in board:
                                    # if clicked_square.get_occupied_piece().is_valid_move(clicked_square,target,board):
                                    #     board.

                            
                        else:
                            if selected_square != clicked_square:
                                # Second Click: Attempt to move selected piece to clicked square
                                piece = selected_square.get_occupied_piece()
                                # print('start_sqaure=', selected_square.get_space())
                                # print('target_sqaure=', clicked_square.get_space())
                                piece.is_valid_move(selected_square, clicked_square, board)
                                
                                if isinstance(piece, Piece) and piece.is_valid_move(selected_square, clicked_square, board):
                                    # Execute Move
                                    taken_piece = clicked_square.get_occupied_piece()
                                    if taken_piece != None and taken_piece.get_colour() != piece.get_colour():
                                        taken_piece = clicked_square.get_occupied_piece()
                                        board.add_captured_piece(taken_piece)
                                        
                                    clicked_square.set_occupied_piece(piece)
                                    piece.set_square(clicked_square)
                                    selected_square.set_occupied_piece(None)
                                    if piece is not None and isinstance(piece, Pawn):
                                        if piece.get_colour() == Colour.WHITE:
                                            if clicked_square.get_row() == 0:
                                                promotion_pawn_square = clicked_square
                                        else:
                                            if clicked_square.get_row() == 7:
                                                promotion_pawn_square = clicked_square
                                    board.switch_turn()

                            # Reset selection after move attempt
                            selected_square = None

    # --- RENDERING BASED ON STATE ---
    if game_state == MENU:
        start_btn_rect = draw_start_menu(screen)
        
    elif game_state == PLAYING:
        draw_board(screen)
        draw_pieces(screen, board)
        draw_captured_pieces(screen, board)
        
    elif game_state == PAUSED:
        # Draw game in background, then draw overlay on top
        draw_board(screen)
        draw_pieces(screen, board)
        draw_captured_pieces(screen, board)
        resume_btn_rect = draw_pause_menu(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()