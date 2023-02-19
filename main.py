import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
API_TOKEN = '5471926329:AAH5Ukkijl_G_KKapyxnI8ReMkPH398f33Q'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Define the game board
game_board = [[None, None, None], [None, None, None], [None, None, None]]


class TicTacToe(StatesGroup):
    waiting_for_move = State()
    game_over = State()


# Function to get the current state of the game board
def get_board(board):
    current_board = "```\n"
    for row in board:
        current_board += " | ".join([sym or " " for sym in row])
        current_board += "\n"
    current_board += "```"
    return current_board


# Function to check if there's a winner
def check_winner(board):
    # Check for horizontal wins
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return True, row[0]

    # Check for vertical wins
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return True, board[0][col]

    # Check for diagonal wins
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return True, board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return True, board[0][2]

    # If there's no winner yet, check if the board is full
    if all(all(row) for row in board):
        return True, "tie"

    # If no winner and the board isn't full, the game is still ongoing
    return False, None


# Start the game
@dp.message_handler(commands='start')
async def start_game(message: types.Message):
    # Reset the game board
    global game_board
    game_board = [[None, None, None], [None, None, None], [None, None, None]]

    # Show the initial game board
    board_text = get_board(game_board)
    await message.answer(board_text)

    # Ask the first player to make a move
    await message.answer("Player 1 (X), make your move.\n"
                         "Enter row and column (e.g. 1 2):")
    await TicTacToe.waiting_for_move.set()


# Player makes a move
@dp.message_handler(state=TicTacToe.waiting_for_move)
async def player_move(message: types.Message, state: FSMContext):
    # Parse the row and column values
    row: object
    row, col = message.text.split()
    row = int(row) - 1
    col = int(col) - 1

    # Check if the move is valid
    if game_board[row][col] is not None:
        await message.answer("Invalid move. That square is already taken. Try again.")
        return

    # Update the game
