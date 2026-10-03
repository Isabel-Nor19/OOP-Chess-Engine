"""Environment diagnostic script for verifying imports and working directory path."""
import os

from ChessBoard import ChessBoard
from Colour import Colour
from Piece import Piece
from Square import Square

print("--- DEBUGGING PYTHON ENVIRONMENT ---")
print(f"Current Working Directory: {os.getcwd()}")
print(f"Files inside this directory: {os.listdir('.')}")

try:
    import Colour
    print(f"SUCCESS: Imported a module named 'colour' from: {Colour.__file__}")
except Exception as e:
    print(f"FAILED to import 'colour': {e}")