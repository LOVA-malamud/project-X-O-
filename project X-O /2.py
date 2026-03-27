def create_board():
    board = []
    for i in range (1, 11):
        board.append(i)
    return board
def print_board(board):
    print(f" {board[0]} | {board[1]} | {board[2]} \n"
          f"---+---+---\n"
          f" {board[3] } | {board[4]} | {board[5]} \n"
          "---+---+---\n"
          f" {board[6]} | {board[7]} | {board[8]} \n")


def get_move(player, board):
    x = 'X'
    o = 'O'

    raw_input = input(f"Player {player}, choose a number between 1 and 9: ")
    if not raw_input.isdigit():
        print("Come on, that's not even a number!")
        return get_move(player, board)

    player_move = int(raw_input)

    if player_move < 1 or player_move > 9:
        print("Hey! That's not between 1 and 9!")
        return get_move(player, board)


    if board[player_move - 1] == x or board[player_move - 1] == o:
        print("Someone's already there!")
        return get_move(player, board)

    return player_move


def make_move(board, position, symbol):
    board[position -1] = symbol
    return board
print(create_board())
print_board(create_board())

print(get_move('X', create_board()))