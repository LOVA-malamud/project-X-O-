import random


def create_board():
    return ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def print_board(board, x_wins, o_wins, ties):
    print(f" score | X: {x_wins} | O: {o_wins} | Ties: {ties}")
    print("=" * 25)
    print(f"  {board[0]} | {board[1]} | {board[2]} ")
    print(" ---+---+---")
    print(f"  {board[3]} | {board[4]} | {board[5]} ")
    print(" ---+---+---")
    print(f"  {board[6]} | {board[7]} | {board[8]} ")
    print("=" * 25 + "\n")


def get_move(player, board):
    while True:
        move_input = input(f"player {player}, pick 1-9 or 'q' to quit: ")

        if move_input == 'q':
            return 'q'

        if not move_input.isdigit():
            print("that's not a number. try again.")
            continue

        pos = int(move_input)
        if pos < 1 or pos > 9:
            print("choose between 1 and 9.")
            continue

        if board[pos - 1] == "X" or board[pos - 1] == "O":
            print("spot taken Pick another.")
            continue

        return pos


def get_computer_move(board):
    available = []
    for i in range(9):
        if board[i] != "X" and board[i] != "O":
            available.append(i + 1)

    if available:
        return random.choice(available)
    return None


def make_move(board, pos, sym):
    board[pos - 1] = sym


def check_winner(board, sym):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
    ]
    for w in wins:
        if board[w[0]] == sym and board[w[1]] == sym and board[w[2]] == sym:
            return True
    return False


def is_tie(board):
    for spot in board:
        if spot != "X" and spot != "O":
            return False
    return True


def switch_player(current):
    if current == "X":
        return "O"
    else:
        return "X"


def play_game():
    print("welcome to tic-tac-toe!")
    x_wins = 0
    o_wins = 0
    ties = 0

    while True:
        print("\n--- MENU ---")
        print("1. two players")
        print("2. play computer")
        print("3. exit")
        choice = input("select an option: ")

        if choice == '3':
            break

        vs_computer = (choice == '2')
        board = create_board()
        current_player = "X"
        game_on = True

        while game_on:
            print_board(board, x_wins, o_wins, ties)

            if vs_computer and current_player == "O":
                print("computer is thinking...")
                move = get_computer_move(board)
            else:
                move = get_move(current_player, board)

            if move == 'q':
                print("exiting match...")
                game_on = False
                continue

            make_move(board, move, current_player)

            if check_winner(board, current_player):
                print_board(board, x_wins, o_wins, ties)
                print(f"player {current_player} wins!")
                if current_player == "X":
                    x_wins += 1
                else:
                    o_wins += 1
                game_on = False
            elif is_tie(board):
                print_board(board, x_wins, o_wins, ties)
                print("its a tie!")
                ties += 1
                game_on = False
            else:
                current_player = switch_player(current_player)

        replay = input("\nplay again? yes/no: ").lower()
        if replay != 'y' and replay != 'yes':
            break

    print(f"\nfinal scores - X: {x_wins} | O: {o_wins} | ties: {ties}")
    print("goodbye!")


if __name__ == "__main__":
    play_game()