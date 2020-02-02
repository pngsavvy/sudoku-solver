from Gui import Gui
import copy

game_board = [
    [5, 0, 9, 0, 0, 0, 4, 0, 0],
    [7, 0, 8, 3, 0, 4, 9, 0, 0],
    [6, 0, 1, 0, 0, 0, 7, 3, 0],
    [4, 6, 2, 5, 0, 0, 0, 0, 0],
    [3, 8, 5, 7, 2, 0, 6, 4, 9],
    [1, 0, 7, 4, 0, 8, 2, 0, 0],
    [2, 0, 0, 1, 0, 0, 0, 0, 4],
    [0, 0, 3, 0, 4, 0, 0, 8, 7],
    [0, 7, 0, 0, 5, 3, 0, 0, 6]
]

size = 9

def print_solution(board):
    for i in range(size):
        for j in range(size):
            print(board[i][j], end=" ")
        print()

# find the box number that the current item is located in
def locate_block(row, col):

    if row > 5:
        rowSection = "3"
    elif row < 3:
        rowSection = "1"
    else:
        rowSection = "2"

    if col > 5:
        colSection = "3"
    elif col < 3:
        colSection = "1"
    else:
        colSection = "2"

    # choose the box that it is in
    selectBox = {
        "11": 0,
        "12": 1,
        "13": 2,
        "21": 3,
        "22": 4,
        "23": 5,
        "31": 6,
        "32": 7,
        "33": 8,
    }

    boxKey = rowSection + colSection
    return selectBox.get(boxKey)

def test_box(board, num, row, col):
    blockNumber = locate_block(row, col)

    # first row
    if blockNumber is 0:
        for i in range(3):
            for j in range(3):
                if board[i][j] == num and str(i) + str(j) != str(row) + str(col):
                    return False
    elif blockNumber is 1:
        for i in range(3):
            for j in range(3, 6):
                if board[i][j] == num and str(i) + str(j) != str(row) + str(col):
                    return False
    elif blockNumber is 2:
        for i in range(3):
            for j in range(6, 9):
                if board[i][j] == num and str(i) + str(j) != str(row) + str(col):
                    return False

    # second row
    elif blockNumber is 3:
        for i in range(3, 6):
            for j in range(3):
                if board[i][j] == num and str(i) + str(j) != str(row) + str(col):
                    return False
    elif blockNumber is 4:
        for i in range(3, 6):
            for j in range(3, 6):
                if board[i][j] == num and str(i) + str(j) != str(row) + str(col):
                    return False
    elif blockNumber is 5:
        for i in range(3, 6):
            for j in range(6, 9):
                if board[i][j] == num and str(i) + str(j) != str(row) + str(col):
                    return False

    # third row
    elif blockNumber is 6:
        for i in range(6, 9):
            for j in range(3):
                if board[i][j] == num and str(i) + str(j) != str(row) + str(col):
                    return False
    elif blockNumber is 7:
        for i in range(6, 9):
            for j in range(3, 6):
                if board[i][j] == num and str(i) + str(j) != str(row) + str(col):
                    return False
    elif blockNumber is 8:
        for i in range(6, 9):
            for j in range(6, 9):
                if board[i][j] == num and str(i) + str(j) != str(row) + str(col):
                    return False
    return True

def test_row(board, num, row, col):
    # Start from the left
    for i in range(0, col):
        if board[row][i] == num:
            return False
    # Start from the right
    for i in range(size - 1, col, -1):
        if board[row][i] == num:
            return False
    return True

def test_column(board, num, row, col):
    # check col from top
    for i in range(0, col):
        if board[i][col] == num:
            return False
    # check col from bottom
    for i in range(size - 1, col, -1):
        if board[i][col] == num:
            return False
    return True

def is_solution(board, num, row, col):
    return test_row(board, num, row, col) and test_column(board, num, row, col) and test_box(board, num, row, col)

def has_Empty_Cell(board, attempt):
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                attempt[0] = row
                attempt[1] = col
                return True
    return False

def solve(board):
    # Last empty cell
    attempt = [0, 0]

    if not has_Empty_Cell(board, attempt):
        print("all cells are filled")
        return True

    rowAttempt = attempt[0]
    colAttempt = attempt[1]

    for num in range(1, size + 1):
        # check if cell can work
        if is_solution(board, num, rowAttempt, colAttempt):

            # try tested value for now
            board[rowAttempt][colAttempt] = num

            if (solve(board)):
                return True

            # failed to solve. reset values
            board[rowAttempt][colAttempt] = 0

    # causes backtracking
    return False


solution_board = copy.deepcopy(game_board)


solve(solution_board)

gui = Gui(solution_board, game_board)

while gui.start_gui():
    word = "run gui"






